#! /usr/bin/env python3
# -*- coding:Utf8 -*-


"""IMPRESSION DE LA LISTE DES EVENTS"""
"APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 6"

###########################################
#### Importation fonction et modules : ####
###########################################


import pygame
from pygame.locals import *
from sys import exit


##############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####
##############################################################################


###############################
#### Programme principal : ####
###############################


pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

font = pygame.font.SysFont("arial", 32)
font_height = font.get_linesize()

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.fill((255, 255, 255))

    pressed_keys = pygame.key.get_pressed()
    y = font_height

    for key_constant, pressed in enumerate(pressed_keys):
        if pressed:  # Clé préssée
            key_name = pygame.key.name(key_constant)  # On recup son nom
            # On stock son nom et son index
            text_surface = font.render(key_name +
                                       " pressed {}".format(key_constant),
                                       True, (0, 0, 0))
            screen.blit(text_surface, (8, y))
            y += font_height

    pygame.display.update()
