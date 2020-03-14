#pylint: disable=C

import time
import sys
import pygame
from pygame.locals import *

pygame.init()

width, height = 1920, 1080
backgroundColor = 176, 223, 229
alonzoVel = [0, 0]
done = False

def control(vel, accel, friction):
    keys = pygame.key.get_pressed()
    if keys[K_d]: vel[0] += accel
    if keys[K_a]: vel[0] -= accel
    if keys[K_s]: vel[1] += accel
    if keys[K_w]: vel[1] -= accel

    vel[0] = vel[0]*friction
    vel[1] = vel[1]*friction

screen = pygame.display.set_mode((width, height))
alonzoRight = pygame.image.load("3D Alonzo.png")
alonzoLeft = pygame.transform.flip(alonzoRight)
song = pygame.mixer.music.load("01 Ana Ng.mp3")
alonzoRect = alonzoRight.get_rect()
pygame.mixer.music.play
screen.fill(backgroundColor)

while not done:
    control(alonzoVel, 0.1, 0.99)
    if (alonzoRect.left + alonzoVel[0]) < 0 or (alonzoRect.right + alonzoVel[0]) > width:
        alonzoVel[0] = 0
    if (alonzoRect.top + alonzoVel[1]) < 0 or (alonzoRect.bottom + alonzoVel[1]) > height:
        alonzoVel[1] = 0
    if alonzoVel[0] > 0: alonzo = alonzoRight
    else: alonzo = alonzoLeft
    
    screen.blit(alonzo, alonzoRect)
    alonzoRect = alonzoRect.move(alonzoVel)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True
    pygame.display.flip()
    time.sleep(10 / 1000)