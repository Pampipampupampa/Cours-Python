
#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""RÉALISATION D'UNsE IMAGE AVEC TOUTES LES COULEURS"""
"""APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 4"""

#########################################
### Importation fonction et modules : ###
#########################################


import pygame


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


# ----- Création des Fonctions ----- #


#############################
### Programme principal : ###
#############################

pygame.init()
screen = pygame.display.set_mode((640, 480))
allColor = pygame.Surface((4096, 4096), depth=24)

for r in range(256):
    print(r + 1, "out of 256")
    x = (r & 15) * 256
    y = (r >> 4) * 256
    for g in range(256):
        for b in range(256):
            allColor.set_at((x + g, y + b), (r, g, b))

pygame.image.save(allColor, "Stock/allcolors.bmp")
