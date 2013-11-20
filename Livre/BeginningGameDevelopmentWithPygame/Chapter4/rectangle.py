#! /usr/bin/env python3
# -*- coding:Utf8 -*-


"""UTILISATION DE LA MÉTHODE DRAW DE PYGAME"""
"""APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 4"""

#### Importation fonction et modules : ####


import pygame
from pygame.locals import *
from sys import exit
from random import *
from math import pi


#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####

#### Programme principal : ####

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

#########################
# Création de rectangle #
#########################
# """Utiliser une surface et fill la surface peut être plus rapide que la création
# d'un rectangle"""
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             exit()
#     screen.lock()
#     for count in range(10):
#         randomColor = (randint(0, 255), randint(0, 255), randint(0, 255))
#         randomPos = (randint(0, 639), randint(0, 479))
#         randomSize = (639 - randint(randomPos[0], 639),
#                       479 - randint(randomPos[1], 479))
#         pygame.draw.rect(screen, randomColor, Rect(randomPos, randomSize))
#     screen.unlock()
#     pygame.display.update()


#########################
# Création de polygones #
#########################
# """Comme pour les autres draw on peut ne pas fill la figure en ajoutant une
# épaisseur de bord (ici par exemple j'ai mis 5)"""
# points = []
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             exit()
#         if event.type == MOUSEBUTTONDOWN:
#             points.append(event.pos)
#             screen.fill((255, 255, 255))
#         if len(points) >= 3:
#             pygame.draw.polygon(screen, (0, 255, 0), points, 5)
#             for point in points:
#                 pygame.draw.circle(screen, (0, 0, 255), point, 5)
#     pygame.display.update()


#########################
# Création de cercles   #
#########################
# """Demande la positiondu centre du cercle et son rayon"""
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             exit()
#     screen.lock()
#     for count in range(10):
#         randomColor = (randint(0, 255), randint(0, 255), randint(0, 255))
#         randomPos = (randint(0, 639), randint(0, 479))
#         randomRadius = randint(1, 200)
#         pygame.draw.circle(screen, randomColor, randomPos, randomRadius)
#     screen.unlock()
#     pygame.display.update()


#########################
# Création d'élipses    #
#########################
# """Mêmes arguments que rectangle (cercle dans un rectangle)"""
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             exit()
#     screen.lock()
#     x, y = pygame.mouse.get_pos()
#     screen.fill((255, 255, 255))
#     pygame.draw.ellipse(screen, (0, 255, 0), (0, 0, x, y))
#     screen.unlock()
#     pygame.display.update()


#########################
# Création d'arcs       #
#########################
# """Mêmes arguments que l'éclipse mais avec 2 de plus :
#         angle de début de tracé, angle de fin de tracé
#     Il n'est pas possible de fill cette forme."""
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             exit()
#     x, y = pygame.mouse.get_pos()
#     angle = (x / 639.) * pi * 2.
#     screen.fill((255, 255, 255))
#     pygame.draw.arc(screen, (0, 0, 0), (0, 0, 639, 479), 0, angle)
#     pygame.display.update()


#########################
# Création de segments  #
#########################
# """Demande la position de départ et de fin du segment"""
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             exit()
#     screen.fill((255, 255, 255))
#     mouse_pos = pygame.mouse.get_pos()
#     for x in range(0, 640, 20):
#         pygame.draw.line(screen, (0, 0, 0), (x, 0), mouse_pos)
#         pygame.draw.line(screen, (0, 0, 0), (x, 479), mouse_pos)
#     for y in range(0, 480, 20):
#         pygame.draw.line(screen, (0, 0, 0), (0, y), mouse_pos)
#         pygame.draw.line(screen, (0, 0, 0), (639, y), mouse_pos)
#     pygame.display.update()


#################################
# Création de segments continus #
#################################
"""Boolean détermine si on raccroche le dernier point au premier"""
points = []
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEMOTION:
            points.append(event.pos)
            if len(points) > 100:
                del points[0]
    screen.fill((255, 255, 255))
    if len(points) > 1:
        pygame.draw.lines(screen, (0, 255, 0), False, points, 2)
    pygame.display.update()


###########################################################
# Création de segments continus ou non avec anti aliasing #
###########################################################
"""Voir les 2 groupes précédents et modifier :
        line par aaline
        lines par aalines """
