#pylint: disable=C

import time
import sys
import random
import pygame
from pygame.locals import *

pygame.init()

BLACK = (0, 0, 0)
SKYBLUE = (176, 223, 229)
# MAP = [
# "...............*",
# "..............*.",
# ".............*..",
# "............*...",
# "...........*....",
# "..........*.....",
# ".........*......",
# "........*.......",
# ".......*........",
# "......*.........",
# ".....*..........",
# "....*...........",
# "...*............",
# "..*.............",
# ".*..............",
# "*..............."]

MAP = [
list("...............*"),
list("..............*."),
list(".............*.."),
list("............*..."),
list("...........*...."),
list("..........*....."),
list(".........*......"),
list("........*......."),
list(".......*........"),
list("......*........."),
list(".....*.........."),
list("....*..........."),
list("...*............"),
list("..*............."),
list(".*..............") ]



def keyControl(vel, accel, friction):
    keys = pygame.key.get_pressed()
    if keys[K_d]: vel[0] += accel
    if keys[K_a]: vel[0] -= accel
    if keys[K_s]: vel[1] += accel
    if keys[K_w]: vel[1] -= accel
    vel[0] = vel[0]*friction
    vel[1] = vel[1]*friction

class XboxControl():
    def __init__(self):
        self.xboxJoy = pygame.joystick.Joystick(0)
        self.xboxJoy.init()
        # print("Joystick xboxJoy initialized!")

    def update(self, player, platforms, runSpeed, jumpPower, g):
        player.vel[0] = self.xboxJoy.get_axis(0) * runSpeed
        if self.xboxJoy.get_button(0) == 1 and player.vel[1] == 0: player.vel[1] = -jumpPower
        else: player.vel[1] += g

class Platform(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, coords, color, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x = coords[0]
       self.rect.y = coords[1]

class Player(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, coords, picture):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       self.coords = coords
       self.vel = [0, 0]
       self.image = pygame.image.load(picture)
       self.rect = self.image.get_rect()
       self.rect.x = self.coords[0]
       self.rect.y = self.coords[1]
       self.mask = pygame.mask.from_surface(self.image)

def find_all(searchList, elem):
    start = 0
    indices = []
    for i in range(0, len(searchList)):
        if searchList[i] == elem: indices.append(i)
    return indices

def main():
    pygame.display.set_caption("crab game")
    width, height = 800, 800
    backgroundColor = SKYBLUE
    done = False

    control = XboxControl()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    
    # alonzoRight = alonzo.image
    # alonzoLeft = pygame.transform.flip(alonzo.image, True, False)
    song = pygame.mixer.music.load("02 Nanobots.mp3")
    pygame.mixer.music.play()

    platformList = []
    platformGroup = pygame.sprite.Group()
    random.shuffle(MAP)
    MAP.append("****************")
    for line in MAP:
        print(line)
        for a in find_all(line, '*'):
            platformList.append(Platform([a * 50, MAP.index(line) * 50], BLACK, 50, 50))
    for i in platformList:
        platformGroup.add(i)
    print(len(platformList))

    alonzo = Player([300,200], "3D Alonzo.png")
    while isinstance(pygame.sprite.spritecollideany(alonzo, platformGroup), pygame.sprite.Sprite):
        alonzo.coords = [random.randint(100, 700), random.randint(100, 700)]

    # main game loop:
    while not done:

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: done = True

        screen.fill(backgroundColor)
        control.update(alonzo, platformGroup, 10, 20, 1)
        # keyControl(alonzo.vel, 0.1, 0.99)
        if (alonzo.rect.left + alonzo.vel[0]) < 0 or (alonzo.rect.right + alonzo.vel[0]) > width:
            alonzo.vel[0] = 0
        if (alonzo.rect.top + alonzo.vel[1]) < 0 or (alonzo.rect.bottom + alonzo.vel[1]) > height:
            alonzo.vel[1] = 0
        for i in platformList:
            if i.rect.colliderect(alonzo.rect.move(alonzo.vel[0], 0)): alonzo.vel[0] = 0
            if i.rect.colliderect(alonzo.rect.move(0, alonzo.vel[1])): alonzo.vel[1] = 0
        # if pygame.key.get_pressed()[K_d] : alonzo.image = alonzoRight
        # elif pygame.key.get_pressed()[K_a]: alonzo.image = alonzoLeft
        olist = alonzo.mask.outline()
        pygame.draw.polygon(screen,(200,150,150),olist,0)

        screen.blit(alonzo.image, alonzo.rect)
        for i in platformList:
            screen.blit(i.image, i.rect)
            i.rect = i.rect.move(-alonzo.vel[0], -alonzo.vel[1])
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: done = True
        pygame.display.flip()

        clock.tick(60)

main()
pygame.quit()