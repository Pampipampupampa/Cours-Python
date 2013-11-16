#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""RÉALISATION D'UN TESTEUR DE COULEUR
   FONCTION RÉALISANT UNE MISE À L'ÉCHELLE D'UNE COULEUR"""
"""APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 4"""

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


def createScales(height):
    """Fonction créant 3 surfaces rectangulaires représentant la gamme de
    chaques couleurs :
        1 pixel horizontalement représente une variation de la couleur
        gauche = foncée  ;  droite = claire"""
    redScaleSurface = pygame.surface.Surface((largeur, height))
    greenScaleSurface = pygame.surface.Surface((largeur, height))
    blueScaleSurface = pygame.surface.Surface((largeur, height))
    for x in range(largeur):
        c = int((x / (largeur - 1)) * 255.)
        red = (c, 0, 0)
        green = (0, c, 0)
        blue = (0, 0, c)
        lineRect = Rect(x, 0, 1, height)
        pygame.draw.rect(redScaleSurface, red, lineRect)
        pygame.draw.rect(greenScaleSurface, green, lineRect)
        pygame.draw.rect(blueScaleSurface, blue, lineRect)
    return redScaleSurface, greenScaleSurface, blueScaleSurface


def scaleColor(color, scale):
    """Fonction permettant de réaliser une mise à l'échelle d'une couleur
       Assombrissement pour 0 < scale > 1
       Eclaircissement pour     scale > 1"""
    red, green, blue = color
    red = int(red * scale)
    green = int(green * scale)
    blue = int(blue * scale)
    return red, green, blue


def saturateColor(color):
    """Permet de saturer la couleur en entrée en évitant de dépasser 255"""
    red, green, blue = color
    red = min(red, 255)
    green = min(green, 255)
    blue = min(blue, 255)
    return red, green, blue


#############################
### Programme principal : ###
#############################

# Constantes de l'application
largeur = 640
hauteur = 480
height = 90
rayon = int(height / 4)

# Tuple de la couleur à afficher
color = [127, 127, 127]
pygame.init()
screen = pygame.display.set_mode((largeur, hauteur), 0, 32)
redScale, greenScale, blueScale = createScales(height)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.fill((0, 0, 0))

    screen.blit(redScale, (0, 0))
    screen.blit(greenScale, (0, height))
    screen.blit(blueScale, (0, height * 2))

    x, y = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:
        for component in range(3):
            if y > component * height and y < (component + 1) * height:
                color[component] = int((x / (largeur - 1)) * 255.)
        pygame.display.set_caption("PyGame Color Test - " + str(tuple(color)))

    for component in range(3):
        pos = (int((color[component] / 255.) * (largeur - 1)),
               component * height + rayon * 2)
        pygame.draw.circle(screen, (200, 200, 200), pos, rayon)

    pygame.draw.rect(screen, tuple(color), (0, height * 3, largeur,
                     height * 3))

    pygame.display.update()
