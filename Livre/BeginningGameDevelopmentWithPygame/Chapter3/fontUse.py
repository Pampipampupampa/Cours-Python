#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""UTILISATION DE POLICE DE CARACTÈRE ET IMPRESSION"""
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

name = "Jérémy Bois, ami du petit pampi"

pygame.init()

# Première méthode pour ajouter du texte : utiliser une police du système
font = pygame.font.SysFont("arial", 64)

# On peut vérifier les polices du système avec cette commande
print(pygame.font.get_fonts())
# Seconde méthode pour ajouter du texte : utiliser un fichier ttf existant
# Cette méthode permet de fourni avec le programme la police et ainsi éviter
# les problèmes de compatibilité
"""my_font = pygame.font.Font("my_font.ttf", 16)"""

# Ajoute le texte au buffer (attention une ligne de texte par appel)
# 1er = texte ; 2nd = antialiasing ; 3rd = textColor ; 4rd = backgroundColor
nameSurface = font.render(name, True, (0, 0, 0), (255, 255, 255))
pygame.image.save(nameSurface, "Stock/name.png")
