import sys
import os
import shutil
import pygame
import pygame.camera
from pygame.locals import *
from pygame import time
from PIL import Image
from multiprocessing import Process, Pipe

from roboticsrov.rover_utils import get_data_path
from roboticsrov.roboticsrov_exception import RoboticsrovException
from roboticslogger.logger import Logger

def get_unique_path(file_path, file_type):
    """ Check if a file already exists. If so, increment a counter and try again until it doesn't. Return that final path. """

    image_counter = 0
    picture_exists = os.path.isfile(file_path + str(image_counter) + file_type)

    while picture_exists:
        image_counter += 1
        picture_exists = os.path.isfile(file_path + str(image_counter) + file_type)

    return file_path + str(image_counter) + file_type

def get_camera(camera_id):
    """ Get the 'camera_id'th camera"""

    cam_list = []
    for device in os.listdir('/dev'):
        if device.startswith('video'):
            cam_list.append(device)

    if camera_id in range(len(cam_list)):
        return cam_list[camera_id]
    else:
        return None

def merge (Images, mergeName, file_type):
    """ Merge a number of images from a list """

    OpenImages = []
    for x in Images:
        OpenImages.append(Image.open(x))

    origSize = OpenImages[0].size #Gets the size of the first image in OpenImages
    origwidth = origSize[0] #Gets the width of the first image in OpenImages
    panoWidth = len(OpenImages)*origSize[0] #Creates the new width of the panorama
    panoHeight = origSize[1] #Creates the new height (which should remain unchanged) of the panorama

    #Creating the new panorama image
    Panorama = Image.new(mode = "RGB", size = (panoWidth, panoHeight))

    #Concatenating the images from left to right and pasting them into the panorama
    for x,img in zip(range(len(OpenImages)),OpenImages):
        Panorama.paste(img,(origwidth*x,0))

    path = get_data_path('pictures')

    image_path = get_unique_path(os.path.join(path, mergeName), file_type) 

    #Saving the panorama
    try:
        Panorama.save(image_path)
    except Exception as e:
        logger.send(["err","Error on save panorama to " + image_path + "\n\t" + e.message])
        image_path = None
    
    return image_path

def snapshot (logger, title = "picture", camera_id = 0, resolution=(640, 480), filetype=".jpg"):
    """ Take a snapshot, save to disk, and return the image path.
        Raises RoboticsrovException if no camera found. """

    # init
    pygame.camera.init()
    camera_device = get_camera(camera_id)
    if camera_device:
        logger.send(["info","Taking snapshot with camera {0}".format(camera_device)])
    else:
        logger.send(["err","No camera detected! Cancelling snapshot."])
        raise RoboticsrovException("No camera available.")

    cam = pygame.camera.Camera(os.path.join("/dev", camera_device), resolution)
    cam.start()
    
    # take the picture
    image = cam.get_image()

    # get/make path for image
    image_path = get_data_path('pictures')
    full_path = get_unique_path(os.path.join(image_path, title), filetype)
    
    # save image locally
    try:
        pygame.image.save(image, full_path)
    except Exception as e:
        logger.send(["err", "Error on try to save image to " + full_path + "\n\t" + e.message])
        full_path = None
    
    # deinit
    cam.stop()
    pygame.quit()
    
    return full_path

def panorama (logger, title = "panoramic", camera_id = 0, camera_resolution=(640, 480), filetype=".jpg"):
    """ Take a panoramic image, save to disk, and return the image """

    Delay = 2
    NumOfPics = 6
    AllParts = []
    x = 0

    while (x < NumOfPics):
        AllParts.append(snapshot(logger, title+"_segment_"+str(x), camera_id, camera_resolution, filetype))
        x += 1
        time.delay(Delay*1000)

    return merge(AllParts, title, filetype)

if __name__ == "__main__":
    logger = Logger("snapshot")
    parent_conn, child_conn = Pipe()

    p = Process(target=logger.run, args=(child_conn,))
    p.start()

    print snapshot(parent_conn)
    print panorama(parent_conn)

    parent_conn.send(["done"])
