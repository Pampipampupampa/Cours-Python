#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""FICHIER CONTENNANT L'ENSEMBLE DES CLASSES UTILISÉES"""
"COURS PYGAME SUR LE SDZ"

#########################################
### Importation fonction et modules : ###
#########################################


import pygame
from pygame.locals import *
import pygame.constants

import numpy as np

from dkContantes import *

############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #

class Donkey:
    """Création du personnage principal"""
    def __init__(self, droite, gauche, haut, bas, niveau):
        # On importe les images du héros
        self.droite = pygame.image.load(dkDroite).convert_alpha()
        self.gauche = pygame.image.load(dkGauche).convert_alpha()
        self.haut = pygame.image.load(dkHaut).convert_alpha()
        self.bas = pygame.image.load(dkBas).convert_alpha()
        # On initialise la position du héros : pixel et case
        self.numCaseX = 0
        self.numCaseY = 0
        self.x = 0
        self.y = 0
        # Initialisation image dk vers le haut
        self.deplacement = self.bas
        # Référence au niveau
        self.niveau = niveau

    def deplacer(self, direction):
        """Déplacement du personnage et actualisation de sa représentation"""
        # Mise en mémoire de la nouvelle position lors d'un mouvement à droite
        if direction == 'droite':
            if self.numCaseX < nombreCase - 1:
                if self.niveau.structure[self.numCaseX + 1,
                                         self.numCaseY] != b'm':
                    self.numCaseX += 1
                    self.x = tailleCase * self.numCaseX
            self.deplacement = self.droite
        # Mise en mémoire de la nouvelle position lors d'un mouvement à gauche
        if direction == 'gauche':
            if self.numCaseX > 0:
                if self.niveau.structure[self.numCaseX - 1,
                                         self.numCaseY] != b'm':
                    self.numCaseX -= 1
                    self.x = tailleCase * self.numCaseX
            self.deplacement = self.gauche
        # Mise en mémoire de la nouvelle position lors d'un mouvement en haut
        if direction == 'haut':
            if self.numCaseY > 0:
                if self.niveau.structure[self.numCaseX,
                                         self.numCaseY - 1] != b'm':
                    self.numCaseY -= 1
                    self.y = tailleCase * self.numCaseY
            self.deplacement = self.haut
        # Mise en mémoire de la nouvelle position lors d'un mouvement en bas
        if direction == 'bas':
            if self.numCaseY < nombreCase - 1:
                if self.niveau.structure[self.numCaseX,
                                         self.numCaseY + 1] != b'm':
                    self.numCaseY += 1
                    self.y = tailleCase * self.numCaseY
            self.deplacement = self.bas


class Niveau:
    """Extraction et affichage d'un niveau du jeu"""
    def __init__(self, fichier):
        self.fichier = fichier
        self.structure = 0
        self.recuperation()

    def recuperation(self):
        """Récupère le fichier du niveau"""
        niveau = np.loadtxt(self.fichier, dtype='S')
        self.structure = niveau

    def afficher(self, fenetre):
        """Génère le niveau récupéré <self.structure>"""
        mur = pygame.image.load(imageMur).convert()
        depart = pygame.image.load(imageDepart).convert()
        arrivee = pygame.image.load(imageArrivee).convert_alpha()
        numLigne = 0
        for ligne in self.structure:
            numColonne = 0
            for column in ligne:
                x, y = numLigne * tailleCase, numColonne * tailleCase
                if column == b'd':  # On ajoute l'élément de départ
                    fenetre.blit(depart, (x, y))
                if column == b'a':  # On ajoute l'élément de fin
                    fenetre.blit(arrivee, (x, y))
                if column == b'm':  # On ajoute un mur
                    fenetre.blit(mur, (x, y))
                numColonne += 1
            numLigne += 1


# ----- Création des Fonctions ----- #


#############################
### Programme principal : ###
#############################


if __name__ == '__main__':
    niveau = Niveau("Stock/niveau1.csv")
    print(niveau.structure, )
    niveau.afficher()
