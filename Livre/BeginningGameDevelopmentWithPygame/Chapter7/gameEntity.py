#! /usr/bin/env python3
# -*- coding:Utf8 -*-


"""CLASSE D'UNE ENTITÉ POUR LA BASE D'UNE CLASSE DE MONSTRE AVEC AI"""
"APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 6"

###########################################
#### Importation fonction et modules : ####
###########################################

import sys
sys.path.append('/home/pampi/Documents/Git/Cours-Python/Livre/BeginningGameDevelopmentWithPygame/Stock')
from vector2d import Vector2D
import pygame
from pygame.locals import *
from sys import exit

##############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####
##############################################################################


class GameEntity:
    """Base class for entity development"""
    def __init__(self, world, name, image):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2D(0, 0)
        self.destination = Vector2D(0, 0)
        self.speed = 0
        self.brain = StateMachine()  # Entity brain
        self.id = 0

    def render(self, surface):
        """Posting the entity to the center instead top corner.
           We do this because the entities will be treated as circles
           with a point and a radius which will simplify the math when we need
           to detect interactions with other entities"""
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))

    def process(self, time_passed):
        """time_passed in seconde"""
        self.brain.think()

        if self.speed > 0 and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.getMagnitude()
            heading = vec_to_destination.normalized()
            # Allows to avoid exceeding the destination
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += travel_distance * heading




###############################
#### Programme principal : ####
###############################


