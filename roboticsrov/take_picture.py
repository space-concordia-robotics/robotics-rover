#Going to get feed from webcam
#take a picture/screenshot
#for now: store it
#for later: send over network to basestation
#save as .jpg file



import pygame
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()

cam = pygame.camera.Camera("/dev/video0",(640,480)) #location and resolution needs to be changed
cam.start()
image = cam.get_image()# captures the image

pygame.image.save(image, "picture.jpg")



