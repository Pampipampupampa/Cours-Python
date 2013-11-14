#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""INITIATION À PYGAME ET AUX ÉVÈNEMENTS"""
"APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 3"

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


if __name__ == '__main__':
    pygame.init()
    screenSize = (800, 600)
    screen = pygame.display.set_mode(screenSize, 0, 32)
    font = pygame.font.SysFont("arial", 16)
    fontHeight = font.get_linesize()
    evenText = []

    # Création d'un évènement (simulation d'un utilisateur) : touche espace
    # Touche enfoncée : On utilise des arguments
    myEvent1 = pygame.event.Event(KEYDOWN, key=K_SPACE, mod=0, unicode=u' ')
    # Touche relachée : On peut aussi utilisé un dictionnaire d'arguments
    myEvent2 = pygame.event.Event(KEYDOWN,
                                  {"key": K_SPACE, "mod": 0, "unicode": u' '})
    # On poste les évènements
    pygame.event.post(myEvent1)
    pygame.event.post(myEvent2)

    # On peut aussi créer de nouveaux évènements
    # Minimum à mettre avant la création d'un nouveau event
    CATONKEYBOARD = USEREVENT + 1
    myEventPerso = pygame.event.Event(CATONKEYBOARD, message="Bad cat!")
    pygame.event.post(myEventPerso)

    while True:
        event = pygame.event.wait()
        evenText.append(str(event))

        if event.type == QUIT:
            exit()
        # On intercepte de la même façon les évènements utilisateur
        if event.type == CATONKEYBOARD:
            print(event.message)

        screen.fill((0, 0, 0))
        y = screenSize[1] - fontHeight
        for text in reversed(evenText):
            screen.blit(font.render(text, True, (0, 255, 0)), (0, y))
            y -= fontHeight

        # Affichage de l'image du buffer à l'écran
        pygame.display.update()
