#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""EXEMPLE D'UTILISATION DU MODULE <MIXER> DE PYGAME"""
"COURS PYGAME DU SDZ"

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

def moduleMixer():
    """Exemple d'utilisation du module mixer :
       Maintenir espace pour écouter le son
       Relâcher epace met le son en pause
       Entrée (<Return>) permet de réinitialiser le son à 0"""
    pygame.init()
    pygame.display.set_mode((640, 480))
    son = pygame.mixer.Sound("Stock/magicSword.wav")
    # son.fadeout(300)  # Fondu à 300ms de la fin de l'objet "son"
    # pygame.mixer.fadeout(300)  # Fondu à 300ms de la fin de tout objet Sound
    actif = 0
    continuer = 1  # Permet de conserver le jeu ouvert
    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0  # On quitte l'application
            if event.type == KEYDOWN:  # Activation lors de l'appui
                # Lancement du son
                if actif == 0 and event.key == K_SPACE:
                    son.play()
                    actif = 1  # Son actuellement en lecture
                # Arrêt du son
                if event.key == K_RETURN:
                    son.stop()
                    actif = 0
                # Reprise du son en pause
                if actif == 1 and event.key == K_SPACE:
                    pygame.mixer.unpause()
            # Mise en pause du son
            if event.type == KEYUP and event.key == K_SPACE:
                pygame.mixer.pause()


#############################
### Programme principal : ###
#############################


if __name__ == '__main__':
    moduleMixer()


# On charge les musiques dans une liste de lecture (pas de variable)
pygame.mixer.music.load("musique.wav")
# On peut ensuite rajouter des musiques dans différentes playlist
# (première par défaut)
pygame.mixer.music.queue("instruments.wav")
# On joue la playlist
pygame.mixer.music.play()
# Stoppe la musique et remet à son début
# (pas le début de la playlist mais de la musique)
pygame.mixer.music.stop()
# Mise en pause de la musique
pygame.mixer.music.pause()
# Reprise de la musique
pygame.mixer.music.unpause()
# Rénilise un fondu à 400ms de la fin des musiques
pygame.mixer.music.fadeout(400)
# Retourne la valeur actuel du volume (valeur entre 0 et 1)
volume = pygame.mixer.music.get_volume()
# Met le volume du mixer à 0.5 (50%)
pygame.mixer.music.set_volume(0.5)
