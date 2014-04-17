#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""MODÉLISATION D'UN FONDU ENTRE 2 COULEURS"""
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


def blend_color(color1, color2, blendFactor):
    red1, green1, blue1 = color1
    red2, green2, blue2 = color2
    red = red1 + (red2 - red1) * blendFactor
    green = green1 + (green2 - green1) * blendFactor
    blue = blue1 + (blue2 - blue1) * blendFactor
    return int(red), int(green), int(blue)


#############################
### Programme principal : ###
#############################

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
color1 = (45, 200, 100)
color2 = (155, 12, 222)
factor = 0.

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.fill((255, 255, 255))
    tri = [(0, 120), (639, 100), (639, 140)]
    pygame.draw.polygon(screen, (0, 255, 0), tri)
    pygame.draw.circle(screen, (0, 0, 0), (int(factor * 639.), 120), 10)
    x, y = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:
        factor = x / 639.
        pygame.display.set_caption("PyColor Blend Test - {:.3f}".format(factor))

    color = blend_color(color1, color2, factor)
    pygame.draw.rect(screen, color, (0, 240, 640, 240))

    pygame.display.update()
