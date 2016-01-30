import pygame
import pygame.camera
from pygame.locals import *
from pygame import time

import sys
from PIL import Image

pygame.init()
pygame.camera.init()

import os



##Images is a list obtained from a folder
##mergename is the final name for the panorama
def merge (Images, mergeName):

    OpenImages = []
    for x in Images:
        OpenImages[Images.index(x)] = Image.open(x)

    origSize = OpenImages[0].size #Gets the size of the first image in OpenImages
    origwidth = imageSize[0] #Gets the width of the first image in OpenImages
    panoWidth = OpenImages.length()*origSize[0] #Creates the new width of the panorama
    panoHeight = imageSize[1] #Creates the new height (which should remain unchanged) of the panorama

    #Creating the new panorama image
    Panorama = Image.new('RBG', (panoWidth, panoHeight))

    #Concatenating the images from left to right and pasting them into the panorama
    for x in OpenImages:
        Panorama.paste(OpenImages[x], (origwidth*OpenImages.index(x),0))

    #Saving the panorama
    Panorama.save(mergeName)
    
    return None



##following lines have ben moved INSIDE the snap_picture function!
#cam = pygame.camera.Camera("/dev/video0",(640,480))
#cam location is default for linux (need to double check)
#cam.start()

def snap_picture (NumOfPics = 1, InitialDelay = 0, Delay = 1, Title = "picture", Folder = "folder"):
    "Takes NumOfPics pictures via the webcam with a Delay between each picture.\
     Both the InitialDelay and Delay are in seconds."
    cam = pygame.camera.Camera("/dev/video0",(640,480)) #resolution of camera needs to be confirmed
    cam.start()
    counter = 0
    if NumOfPics == 1:
        time.delay(InitialDelay*1000)
        image = cam.get_image()
        PicName = Title + ".jpg"
        pygame.image.save(image, PicName)
        source = os.getcwd() + "/" + PicName
        #create destination folder and get its path
        try:
            os.makedirs(os.getcwd() + "/" + Folder)
        except OSError as e:
            pass
        finally:
            newpath = os.getcwd() + "/" + Folder
        shutil.move(source, newfilepath)  #need to get the src path for this to work
    elif NumOfPics > 1:
        time.delay(InitialDelay*1000)
        while (NumOfPics > 0):
            counter +=1
            image = cam.get_image()
            PicName = Title + "-" + str(counter) + ".jpg"
            pygame.image.save(image, PicName)
            try:
                os.makedirs(os.getcwd() + "/" + Folder)
            except OSError as e:
                pass
            finally:
                newpath = os.getcwd() + "/" + Folder
            shutil.move(source, newfilepath)
            NumOfPics -= 1 
            time.delay(Delay*1000)
    else:
        pass
    cam.stop()
    return None



def panorama (Title = "pano1"):
    #Get GPS location and input that as Title parameter in snap_picture
    snap_picture(6, 0, 1, Title,"PanoFolder")
    #pull images from where they've been saved and put them in a list
    #that list is the first argument in the merge() function below
    parts = []
    pics = 6
    counter = 1
    while counter <= pics:
        parts.append(Title + "-" + str(counter) + ".jpg")
        counter += 1
    merge(parts,Title)
    return None


