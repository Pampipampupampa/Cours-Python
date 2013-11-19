#! /usr/bin/env python3
# -*- coding:Utf8 -*-


"""INTRUCTIONS À PROPOS DE L'UTILISATION DES SURFACES"""
"""APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 4"""


#### Importation fonction et modules : ####


import pygame
from pygame.locals import *
from sys import exit

#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####




#### Programme principal : ####


pygame.init()
screenSize = (640, 480)
screen = pygame.display.set_mode(screenSize, 0, 32)

# Chargement d'une image avec conversion automatique en fonction de la surface
background = pygame.image.load("Stock/sushiplate.jpg").convert()
# Même chose mais conserve la transparence
background = pygame.image.load("Stock/sushiplate.jpg").convert_alpha()

# Création d'une surface de 256/256 avec couche alpha (depth=32 nécessaire)
# HWSURFACE Creates a hardware surface (plus rapide)
blank_alpha_surface = pygame.Surface((256, 256), flags=SRCALPHA, depth=32)

# Deux façons de construire une surface rectangulaire
my_rect3 = Rect(100, 100, 200, 150)
my_rect4 = Rect((100, 100), (200, 150))

# Création d'un dictionnaire contenant de parties d'une image
# (pratique pour les sprites)
my_font_image = background
letters = {}  # Création d'un dictionnaire et ajout des images dedans
letters["a"] = my_font_image.subsurface((0, 0), (80, 80))
letters["b"] = my_font_image.subsurface((80, 0), (80, 80))

while True:
    # Eviter d'utiliser le CPU lorsque il ne se passe rien
    event = pygame.event.wait()
    if event.type == QUIT:
        exit()
    # Afin d'éviter un effet dit de strobing (conservation anciennes positions
    # des images) on colore le fond
    screen.fill((0, 0, 0))
    # ou on ajoute une image de fond
    screen.blit(background, (0, 0))
    screen.blit(letters["a"], (22, 130))  # Affichage de l'image coupée
    # On choisie une image, sa nouvelle position, et la portion de la dit
    # image que l'on veut afficher à la nouvelle position
    # On peut par exemple ajouter une variable suivant <x> ou <y> afin de
    # récupérer une partie d'une sprite, sans avoir à créer 1000 images
    screen.blit(background, (300, 200), (300, 220, 200, 200))
    pygame.display.update()
