#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""INITIATION À PYGAME BASES"""
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


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption("Hello World !!")
    backImage = pygame.image.load("Stock/sushiplate.jpg").convert()
    mouseImage = pygame.image.load("Stock/fugu.png").convert_alpha()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        screen.blit(backImage, (0, 0))

        # Récupération de la position de la souris
        x, y = pygame.mouse.get_pos()
        x -= mouseImage.get_width() / 2
        y -= mouseImage.get_height() / 2
        screen.blit(mouseImage, (x, y))

        # Affichage de l'image du buffer à l'écran
        pygame.display.update()
