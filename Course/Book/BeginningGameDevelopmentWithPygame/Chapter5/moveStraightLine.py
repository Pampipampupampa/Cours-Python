#! /usr/bin/env python3
# -*- coding:Utf8 -*-


"""INITIATION À LA MISE EN MOUVEMENT SELON UN AXE (x)
DIFFÉRENCES ENTRE FPS ET VITESSE DANS LES JEUX"""
"APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 5"


#### Importation fonction et modules : ####

import pygame
from pygame.locals import *
from sys import exit


#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####

#### Programme principal : ####

background = 'Stock/sushiplate.jpg'
spriteImage = 'Stock/fugu.png'

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
background = pygame.image.load(background).convert()
sprite = pygame.image.load(spriteImage)
# The x coordinate of our sprites
x1 = 0.
x2 = 0.

frame_no = 0

# Our clock object
clock = pygame.time.Clock()
# Speed in pixels per second
speed = 250.

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0, 0))
    screen.blit(sprite, (x1, 50))
    screen.blit(sprite, (x2, 250))
    # Same speed for this two frames but different frame rate
    timePassed = clock.tick(30)
    timePassedSecond = timePassed / 1000.0
    distanceMoved = timePassedSecond * speed
    x1 += distanceMoved
    if (frame_no % 5) == 0:  # Every five frames we move the second sprite
        distanceMoved = timePassedSecond * speed
        x2 += distanceMoved * 5.  # Adjust the distance to the first sprite
    # If the image goes off the end of the screen, move it back
    if x1 > 640.:
        x1 -= 640.
    if x2 > 640.:
        x2 -= 640.
    pygame.display.update()
    frame_no += 1
