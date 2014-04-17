#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""INITIATION À LA MISE EN MOUVEMENT SELON 2 AXES (x et y)"""
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
x, y = 100., 100.

# Speed
speedX, speedY = 133., 170.

# Our clock object
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0, 0))
    screen.blit(sprite, (x, y))
    timePassed = clock.tick(30)
    timePassedSecond = timePassed / 1000.0
    x += speedX * timePassedSecond
    y += speedY * timePassedSecond
    # If the sprite goes off the edge of the screen,
    # make it move in the opposite direction
    if x > 640 - sprite.get_width():
        speedX = -speedX
        x = 640 - sprite.get_width()
    elif x < 0:
        speedX = -speedX
        x = 0.
    if y > 480 - sprite.get_height():
        speedY = -speedY
        y = 480 - sprite.get_height()
    elif y < 0:
        speedY = -speedY
        y = 0

    pygame.display.update()
