#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""INITIATION À PYGAME ET AUX ÉVÈNEMENTS : MOUVEMENT DU BACKGROUND"""
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

    # Montre l'ensemble des résolutions disponibles sur l'ordinateur
    print(pygame.display.list_modes())

    screen = pygame.display.set_mode((640, 480), 0, 32)
    background = pygame.image.load("Stock/sushiplate.jpg").convert()
    x, y = 0, 0
    move_x, move_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_x = -1
                elif event.key == K_RIGHT:
                    move_x = +1
                elif event.key == K_UP:
                    move_y = -1
                elif event.key == K_DOWN:
                    move_y = +1
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    move_x = 0
                elif event.key == K_RIGHT:
                    move_x = 0
                elif event.key == K_UP:
                    move_y = 0
                elif event.key == K_DOWN:
                    move_y = 0

        # On ajoute à <x> et <y> la valeur de <move_x> et <move_y>
        x += move_x
        y += move_y
        # On actualise la couleur sous l'image de fond
        screen.fill((255, 255, 255))
        # On modifie la position du fond
        screen.blit(background, (x, y))

        # Affichage de l'image du buffer à l'écran
        pygame.display.update()
