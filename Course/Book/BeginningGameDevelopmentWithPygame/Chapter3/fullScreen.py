#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PASAGE EN PLEIN ÉCRAN SOUS PYGAME"""
"APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 3"

#########################################
### Importation fonction et modules : ###
#########################################


import pygame
from pygame.locals import *
from sys import exit


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


# ----- Création des Fonctions ----- #


#############################
### Programme principal : ###
#############################

backImage = 'Stock/sushiplate.jpg'

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
background = pygame.image.load(backImage).convert()
fullscreen = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((640, 480), FULLSCREEN,
                                                     32)
                else:
                    screen = pygame.display.set_mode((640, 480), 0, 32)

    screen.blit(background, (0, 0))
    pygame.display.update()
