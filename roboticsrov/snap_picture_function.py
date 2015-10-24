import pygame
import pygame.camera
from pygame.locals import *
from pygame import time

pygame.init()
pygame.camera.init()

##following lines have ben moved INSIDE the snap_picture function!
#cam = pygame.camera.Camera("/dev/video0",(640,480))
#cam location is default for linux (need to double check)
#cam.start()

def snap_picture (NumOfPics = 1, InitialDelay = 0, Delay = 1, Title = "picture"):
    "Takes NumOfPics pictures via the webcam with a Delay between each picture.\
     Both the InitialDelay and Delay are in seconds."
    cam = pygame.camera.Camera("/dev/video0",(640,480)) #resolution of camera needs to be confirmed
    cam.start()
    counter = 0
    if NumOfPics == 1:
        time.delay(InitialDelay*1000)
        image = cam.get_image()
        PicName = Title + ".jpg"
        pygame.image.save(image, PicName) #image needs to be networked to basestation before saving
    elif NumOfPics > 1:
        time.delay(InitialDelay*1000)
        while (NumOfPics > 0):
            counter +=1
            image = cam.get_image()
            PicName = Title + "-" + str(counter) + ".jpg"
            pygame.image.save(image, PicName) #image needs to be networked to basestation before saving
            NumOfPics -= 1 
            time.delay(Delay*1000)
    else:
        pass
    return None


def panorama ():
    #Get GPS location and input that as Title parameter in snap_picture
    snap_picture(6, 0, 1, "Panorama")
    #get images from cwd and put them together 
    return None


