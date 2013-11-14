#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""GENERATE MULTI BACKGROUND SURFACES"""
"""APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 3"""

"""If you use a double-buffered display, you should call pygame.display.flip()
rather than pygame.display.update(). This does the instant display switch
rather than copying screen data"""

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


screenSize = (640, 480)
pygame.init()
screen = pygame.display.set_mode(screenSize, RESIZABLE, 32)
background = pygame.image.load("Stock/sushiplate.jpg").convert()

while True:
    # Eviter d'utiliser le CPU lorsque il ne se passe rien
    event = pygame.event.wait()
    if event.type == QUIT:
        exit()
    if event.type == VIDEORESIZE:
        # Récupère la taille de la fenêtre dans l'event VIDEORESIZE
        screenSize = event.size
        screen = pygame.display.set_mode(screenSize, RESIZABLE, 32)
        pygame.display.set_caption("Window resized to " + str(event.size))

    screenWidth, screenHeight = screenSize

    # Permet de dupliquer le fond d'écran afin qu'ils couvrent l'ensemble du
    # fond de la fenêtre sans recoupement
    for y in range(0, screenHeight, background.get_height()):
        for x in range(0, screenWidth, background.get_width()):
            screen.blit(background, (x, y))

    pygame.display.update()
