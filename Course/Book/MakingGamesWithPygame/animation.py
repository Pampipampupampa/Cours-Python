#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""SHORT ANIMATION"""
"MAKING GAMES WITH PYGAME : CHAPTER 2 - BASICS"

###########################################
#### Importation fonction et modules : ####
###########################################

import sys
sys.path.append('/home/pampi/Documents/Git/Cours-Python/Library')
from vector2d import *
import pygame
from pygame.locals import *

##############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####
##############################################################################

###############################
#### Programme principal : ####
###############################


WHITE = (255, 255, 255)

pygame.init()

DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Animation')

cat = pygame.image.load("Stock/cat.png")
cat_pos = Vector2D(10, 10)
cat_speed = 150
cat_direction = Vector2D(1, 0)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    # Keep the cat around the screen
    if cat_pos[0] > 400 - cat.get_width():
        cat_pos[0] = 400 - cat.get_width()  # To avoid conflicts
        cat_direction = Vector2D(0, 1)

    elif cat_pos[0] < 10:
        cat_pos[0] = 10  # To avoid conflicts
        cat_direction = Vector2D(0, -1)

    elif cat_pos[1] > 300 - cat.get_height():
        cat_pos[1] = 300 - cat.get_height()  # To avoid conflicts
        cat_direction = Vector2D(-1, 0)

    elif cat_pos[1] < 10:
        cat_pos[1] = 10  # To avoid conflicts
        cat_direction = Vector2D(1, 0)

    time_passed_seconds = clock.tick(30) / 1000.0
    cat_pos += time_passed_seconds * cat_direction * cat_speed

    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(cat, cat_pos)
    pygame.display.update()
