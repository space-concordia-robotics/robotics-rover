import pygame
import pygame.camera
from pygame.locals import *
from pygame import time

import sys
from PIL import Image

pygame.init()
pygame.camera.init()

import os
import shutil



##Images is a list obtained from a folder
##mergename is the final name for the panorama
def merge (Images, mergeName):

    OpenImages = []
    for x in Images:
        OpenImages.append(Image.open(x))

    origSize = OpenImages[0].size #Gets the size of the first image in OpenImages
    origwidth = origSize[0] #Gets the width of the first image in OpenImages
    panoWidth = len(OpenImages)*origSize[0] #Creates the new width of the panorama
    panoHeight = origSize[1] #Creates the new height (which should remain unchanged) of the panorama

    #Creating the new panorama image
    Panorama = Image.new(mode = "RGB",size = (panoWidth, panoHeight))

    #Concatenating the images from left to right and pasting them into the panorama
    for x,img in zip(range(len(OpenImages)),OpenImages):
        Panorama.paste(img,(origwidth*x,0))

    #Saving the panorama
    Panorama.save(mergeName + ".jpg")
    
    return Panorama



##following lines have ben moved INSIDE the snap_picture function!
#cam = pygame.camera.Camera("/dev/video0",(640,480))
#cam location is default for linux (need to double check)
#cam.start()

def snapshot (NumOfPics = 1, InitialDelay = 0, Delay = 1, Title = "picture", Folder = "folder"):
    "Takes NumOfPics pictures via the webcam with a Delay between each picture.\
     Both the InitialDelay and Delay are in seconds."
    cam = pygame.camera.Camera("/dev/video0",(640,480)) #resolution of camera needs to be confirmed
    cam.start()
    counter = 0
    if NumOfPics == 1:
        time.delay(InitialDelay*1000)
        image = cam.get_image()
        PicName = Title + ".jpg"
        #check if another file with the title already exists
            #save all titles to a file? and check from there?
        #if it does, add a number at the end of it
            #make recursive.
            #if -1 exists, check if -2 exists, etc until you hit the end then tac on the next number
        pygame.image.save(image, PicName)
        source = os.getcwd() + "/" + PicName
        try:
            os.makedirs(os.getcwd() + "/" + Folder)
        except OSError as e:
            pass
        finally:
            newpath = os.getcwd() + "/" + Folder
        shutil.move(source, newpath)
    elif NumOfPics > 1:
        time.delay(InitialDelay*1000)
        while (NumOfPics > 0):
            counter +=1
            image = cam.get_image()
            PicName = Title + "-" + str(counter) + ".jpg"
            pygame.image.save(image, PicName)
            source = os.getcwd() + "/" + PicName
            try:
                os.makedirs(os.getcwd() + "/" + Folder)
            except OSError as e:
                pass
            finally:
                newpath = os.getcwd() + "/" + Folder
            shutil.move(source, newpath)
            NumOfPics -= 1 
            time.delay(Delay*1000)
    else:
        pass
    cam.stop()
    return None



def panorama (Title = "pano", Folder = "PanoFolder"):
    #assumes the camera rotates clockwise
    #Get GPS location and input that as Title parameter in snap_picture
    cam = pygame.camera.Camera("/dev/video0",(640,480)) #resolution of camera needs to be confirmed
    cam.start()
    InitialDelay = 1
    Delay = 2
    NumOfPics = 6
    AllParts = []
    time.delay(InitialDelay*1000)
    
    while (NumOfPics > 0):
        counter +=1
        image = cam.get_image()
        PicName = Title + "-" + str(counter) + ".jpg"
        pygame.image.save(image, PicName)
        source = os.getcwd() + "/" + PicName
        try:
            os.makedirs(os.getcwd() + "/" + Folder)
        except OSError as e:
            pass
        finally:
            newpath = os.getcwd() + "/" + Folder
        shutil.move(source, newpath)
        NumOfPics -= 1 
        time.delay(Delay*1000)
    cam.stop()

    picsToAppend = 6
    counter = 1
    while counter <= picsToApend:
        AllParts.append(Folder + "/" + Title + "-" + str(counter) + ".jpg")
        counter += 1
    return merge(AllParts,Title)


