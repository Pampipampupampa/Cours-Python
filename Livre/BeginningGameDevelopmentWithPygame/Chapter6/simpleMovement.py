#! /usr/bin/env python3
# -*- coding:Utf8 -*-

"""MOUVEMENT UNIDIRECTIONNELS"""
"APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 6"

###########################################
#### Importation fonction et modules : ####
###########################################

import sys
sys.path.append('/home/pampi/Documents/Git/Cours-Python/Livre/BeginningGameDevelopmentWithPygame/Stock')
import pygame
from pygame.locals import *
from sys import exit
from vector2d import Vector2D


##############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####
##############################################################################


###############################
#### Programme principal : ####
###############################


back = 'Stock/sushiplate.jpg'
sprite = 'Stock/fugu.png'


pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)

background = pygame.image.load(back).convert()
sprite = pygame.image.load(sprite).convert_alpha()

clock = pygame.time.Clock()

spritePos = Vector2D(200, 150)
spriteSpeed = 300.

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    pressed_keys = pygame.key.get_pressed()
    # Le vecteur permet de stocke une information en x et en y ( ---> diag)
    direction = Vector2D(0, 0)
    if pressed_keys[K_LEFT]:
        direction[0] = -1
    elif pressed_keys[K_RIGHT]:
        direction[0] = +1
    if pressed_keys[K_UP]:
        direction[1] = -1
    elif pressed_keys[K_DOWN]:
        direction[1] = +1
    # On normalise le vecteur pour uniformiser le mouvement
    # (vitesse en diag == vitesse ligne droite)
    direction.normalize()

    screen.blit(background, (0, 0))
    screen.blit(sprite, spritePos)
    # Uniformiation de la vitesse de la sprite en fonction du processeur
    time_passed = clock.tick(30)
    time_passed_seconds = time_passed / 1000.0
    spritePos += direction * spriteSpeed * time_passed_seconds
    pygame.display.update()
