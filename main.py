
import pygame
import time
import sys

pygame.init()
width, height = 800, 600
backgroundColor = 255, 0, 0
alonzoVel = [2, -1]

screen = pygame.display.set_mode((width, height))
alonzo = pygame.image.load("3D Alonzo.png")
alonzoRect = alonzo.get_rect()


while True:
    if alonzoRect.left < 0 or alonzoRect.right > width:
        alonzoVel[0] = -alonzoVel[0]
    if alonzoRect.top < 0 or alonzoRect.bottom > height:
        alonzoVel[1] = -alonzoVel[1]

    screen.fill(backgroundColor)

    screen.blit(alonzo, alonzoRect)
    alonzoRect = alonzoRect.move(alonzoVel)

    pygame.display.flip()
    time.sleep(10 / 1000)

