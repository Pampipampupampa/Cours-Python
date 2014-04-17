#! /usr/bin/env python3
# -*- coding:Utf8 -*-


"""PIXELISATION D'UNE FENÊTRE PYGAME PIXEL PAR PIXEL ALÉATOIREMENT"""
"""APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 4"""


#### Importation fonction et modules : ####

import pygame
from pygame.locals import *
from sys import exit
from random import randint

#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####




#### Programme principal : ####


pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    randCoul = (randint(0, 255), randint(0, 255), randint(0, 255))
    # Lorsque on va utiliser une surface pour faire un long dessin par exemple,
    # on peut utiliser la fonction lock pour éviter à pygame de lock unlock
    # durant la boucle (augmente fortement la vitesse)
    screen.lock()
    for _ in range(100):
        randPos = (randint(0, 639), randint(0, 479))
        # Méthode utilisée pour choisir le pixel
        screen.set_at(randPos, randCoul)
        # Sélectionner un pixel de l'écran
        myColor = screen.get_at((100, 100))
    screen.unlock()
    pygame.display.update()
