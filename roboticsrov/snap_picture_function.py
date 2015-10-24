import pygame
import pygame.camera
from pygame.locals import *
from pygame import time

pygame.init()
pygame.camera.init()

#cam = pygame.camera.Camera("/dev/video0",(640,480)) #location and resolution needs to be changed (?)
#cam location is default for linux (need to double check)
#cam.start()

def snap_picture (NumOfPics = 1, InitialDelay = 0, Delay = 1, Title = "picture"):
    "Takes NumOfPics pictures via the webcam with a Delay between each picture.\
     Both the InitialDelay and Delay are in seconds."
    cam = pygame.camera.Camera("/dev/video0",(640,480))
    cam.start()
    counter = 0
    if NumOfPics == 1:
        time.delay(InitialDelay*1000)
        image = cam.get_image()
        pygame.image.save(image, Title)
    elif NumOfPics > 1:
        time.delay(InitialDelay*1000)
        while (NumOfPics > 0):
            counter +=1
            image = cam.get_image()
            PicName = Title + str(counter)
            #create string that holds pictures names (e.g. pic1, pic2, pic3, pic4, etc)
            pygame.image.save(image, PicName)
            NumOfPics -= 1 
            time.delay(Delay*1000)
    else:
        pass
    return null


