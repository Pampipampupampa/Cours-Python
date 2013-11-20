#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""INITIATION À PYGAME"""
"PART 1 : SDZ"

#########################################
### Importation fonction et modules : ###
#########################################


import pygame
from pygame.locals import *
import pygame.constants

############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


# ----- Création des Fonctions ----- #


#############################
### Programme principal : ###
#############################


pygame.init()  # Initialisation de pygame
pygame.key.set_repeat(400, 30)  # Activation du clic enfoncé

# Affichage de la fenêtre
fenetre = pygame.display.set_mode((640, 480), RESIZABLE)

# Importation et convertion du fond aux dimensions de la fenêtre
fond = pygame.image.load("Stock/background.jpg").convert()
fenetre.blit(fond, (0, 0))  # Placement du fond importé

# Ajout du personnage en conservant la zone transparente (noire sinon)
perso = pygame.image.load("Stock/perso.png").convert_alpha()

# Rendre une couleur spécifique transparente
# perso.set_colorkey((129, 164, 96))  # le blanc de l'image devient transparent


#########################################################
################# Variante avec la souris #################
#########################################################

# # On place le personnage en fonction de la position du personnage
# persoX = 0
# persoY = 0
# fenetre.blit(perso, (persoX, persoY))  # Initialisation en haut à gauche


# # Rafraichissement permettant l'affichage des changements (affichage du fond)
# pygame.display.flip()


# # Boucle infinie permettant de garder le programme ouvert
# continuer = 1
# #Boucle infinie
# while continuer:
#     # On parcours la liste de tous les événements reçus
#     for event in pygame.event.get():
#         if event.type == QUIT:     # Si un de ces événements est de type QUIT
#             continuer = 0      # On arrête la boucle
#         # if event.type == KEYDOWN:
#         #     if event.key == K_DOWN:  # Si "flèche bas"
#         #         # On descend le perso
#         #         position_perso = position_perso.move(0, 10)
#         #     if event.key == K_UP:  # Si "flèche bas"
#         #         # On descend le perso
#         #         position_perso = position_perso.move(0, -10)
#         #     if event.key == K_LEFT:  # Si "flèche bas"
#         #         # On descend le perso
#         #         position_perso = position_perso.move(-10, 0)
#         #     if event.key == K_RIGHT:  # Si "flèche bas"
#         #         # On descend le perso
#         #         position_perso = position_perso.move(10, 0)
#         if event.type == MOUSEBUTTONDOWN:
#             if event.button == 1:  # Si clic gauche
#                 #On change les coordonnées du perso
#                 persoX = event.pos[0]
#                 persoY = event.pos[1]
#         # if event.type == MOUSEMOTION:  # Si mouvement de souris
#         #         # On change les coordonnées du perso
#         #         persoX = event.pos[0]
#         #         persoY = event.pos[1]
#         # On remet le fond puis le perso
#         fenetre.blit(fond, (0, 0))  # Placement du fond importé
#         fenetre.blit(perso, (persoX, persoY))


#########################################################
################# Variante avec le clavier #################
#########################################################

# On récupère la position du perso
position_perso = perso.get_rect()

# On place le personnage en fonction de la position du personnage
fenetre.blit(perso, position_perso)  # Initialisation en haut à gauche


# Rafraichissement permettant l'affichage des changements (affichage du fond)
pygame.display.flip()


# Boucle infinie permettant de garder le programme ouvert
continuer = 1
#Boucle infinie
while continuer:
    # On parcours la liste de tous les événements reçus
    for event in pygame.event.get():
        if event.type == QUIT:     # Si un de ces événements est de type QUIT
            continuer = 0      # On arrête la boucle
        if event.type == KEYDOWN:
            if event.key == K_DOWN:  # Si "flèche bas"
                # On descend le perso
                position_perso = position_perso.move(0, 10)
            if event.key == K_UP:  # Si "flèche bas"
                # On descend le perso
                position_perso = position_perso.move(0, -10)
            if event.key == K_LEFT:  # Si "flèche bas"
                # On descend le perso
                position_perso = position_perso.move(-10, 0)
            if event.key == K_RIGHT:  # Si "flèche bas"
                # On descend le perso
                position_perso = position_perso.move(10, 0)
        # On remet le fond puis le perso
        fenetre.blit(fond, (0, 0))  # Placement du fond importé
        fenetre.blit(perso, position_perso)

##############################################
####################Commun####################
##############################################

        #Rafraichissement
        pygame.display.flip()
