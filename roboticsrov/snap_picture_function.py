import pygame
import pygame.camera
from pygame.locals import *
from pygame import time

import sys
from PIL import Image

import os
import shutil

def file_exists_increment_counter(file_path, file_type, logger):
    """ Check if a file already exists. If so, increment a counter and try again until it doesn't. Return that final path. """

    picture_exists = os.path.isfile(file_path + file_type)
    image_counter = 0

    while picture_exists:
        image_counter += 1
        picture_exists = os.path.isfile(file_path + str(image_counter) + file_type)

    return file_path + str(image_counter) + file_type

def get_camera(camera_id, logger):
    """ Get the 'camera_id'th camera"""
    cam_list = []
    for device in os.listdir('/dev'):
        if device.startswith('video'):
            cam_list.append(device)

    if camera_id in range(len(cam_list)):
        logger.send(["info","Got camera at #{0}: {1}".format(camera_id, cam_list[camera_id])])
        return cam_list[camera_id]
    else:
        logger.send(["err","Could not find camera #{0}".format(camera_id)])
        return None


def merge (Images, mergeName, file_type, logger):
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

    path = get_data_path('pictures', logger)

    image_path = file_exists_increment_counter(os.path.join(path, mergeName), file_type, logger) 

    #Saving the panorama
    Panorama.save(image_path)
    
    return image_path

def snapshot (title = "picture", camera_id = 0, resolution=(640, 480), filetype=".jpg", logger):
    """ Take a snapshot, save to disk, and return the image path """

    # init
    pygame.camera.init()
    cam = pygame.camera.Camera(os.path.join("/dev", get_camera(camera_id)), resolution)
    cam.start()
    
    # take the picture
    image = cam.get_image()

    # get/make path for image
    image_path = get_data_path('pictures', logger)
    
    # get counter if image already exists
    file_exists_increment_counter
    picture_exists = False
    image_counter = 0
    while not picture_exists:
        image_counter += 1
        picture_exists = not os.path.isfile(os.path.join(image_path, title + str(image_counter) + filetype))

    full_path = os.path.join(image_path, title + str(image_counter) + filetype)
    
    # save image locally
    try:
        pygame.image.save(image, full_path)
    except Exception as e:
        logger.send(["err", "Error on try to save image to " + full_path + "\n\t" + e.message])
    
    # deinit
    cam.stop()
    pygame.quit()
    
    return full_path

def panorama (title = "panoramic", camera_id = 0, camera_resolution=(640, 480), filetype=".jpg", logger):
    """ Take a panoramic image, save to disk, and return the image """

    Delay = 2
    NumOfPics = 6
    AllParts = []

    while (x < NumOfPics):
        AllParts.append(snapshot(title+str(NumOfPics), camera_id, camera_resolution, filetype))
        x += 1
        time.delay(Delay*1000)

    return merge(AllParts, title)
