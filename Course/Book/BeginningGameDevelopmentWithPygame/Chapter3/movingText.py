#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""RÉALISATION D'UN TEXTE QUI BOUGE"""
"""APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 3"""

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
screenSize = (640, 480)
message = "Test de l'animation du texte"

pygame.init()
screen = pygame.display.set_mode(screenSize)
font = pygame.font.SysFont("arial", 20)
textSurface = font.render(message, True, (0, 0, 255))

x = screenSize[0]
y = (screenSize[1] - textSurface.get_height()) / 2
background = pygame.image.load(backImage).convert()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0, 0))
    x -= 2
    if x < -textSurface.get_width():  # Largeur du texte pas de la fenêtre
        x = screenSize[0]

    screen.blit(textSurface, (x, y))
    screen.blit(textSurface, (x + textSurface.get_width(), y))
    pygame.display.update()
