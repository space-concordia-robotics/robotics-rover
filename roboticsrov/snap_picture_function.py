import pygame
import pygame.camera
from pygame.locals import *
from pygame import time

pygame.init()
pygame.camera.init()

cam = pygame.camera.Camera("/dev/video0",(640,480)) #location and resolution needs to be changed (?)
#cam location is default for linux (need to double check)
cam.start()

def snap_picture (NumOfPics = 1, InitialDelay = 0, Delay = 1):
    "Takes NumOfPics pictures via the webcam with a Delay between each picture.\
     Both the InitialDelay and Delay are in seconds."
    if NumOfPics == 1:
        time.delay(InitialDelay*1000)
        image = cam.get_image()
        #create string that holds picture name (possibly via input)
        Title = input("What is the name of this picture? Please also add the approproate file extension:  ")
        pygame.image.save(image, Title)
    elif NumOfPics > 1:
        time.delay(InitialDelay*1000)
        for (NumOfPics > 0):
            image = cam.get_image()
            #create string that holds pictures names (e.g. pic1, pic2, pic3, pic4, etc)
            pygame.image.save(image, "picture.jpg") 
            time.delay(Delay*1000)
    else:
        break
    return null


