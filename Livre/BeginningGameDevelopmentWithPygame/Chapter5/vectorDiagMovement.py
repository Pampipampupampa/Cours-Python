#! /usr/bin/env python3
# -*- coding:Utf8 -*-


"""CRÉATION D'UN MOUVEMENT DIAGONAL GRÂCE AUX VECTEURS"""
"APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 5"

#
# Importation fonction et modules : ####
#
import sys
sys.path.append('/home/pampi/Documents/Git/Cours-Python/Livre/BeginningGameDevelopmentWithPygame/Stock')
import pygame
from pygame.locals import *
from sys import exit
from vector2d import Vector2D

#
# Gestion d'évènements : définition de différentes Fonctions/Classes : ####
#


#
# Programme principal : ####
#
pygame.init()
background_image_filename = 'Stock/sushiplate.jpg'
sprite_image_filename = 'Stock/fugu.png'

screen = pygame.display.set_mode((640, 480), 0, 32)
background = pygame.image.load(background_image_filename).convert()
sprite = pygame.image.load(sprite_image_filename).convert_alpha()

clock = pygame.time.Clock()
position = Vector2D(100.0, 100.0)
speed = 250.
heading = Vector2D()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            #
            #
            # <*> juste avant un paramètre de fonction permet d'étendre le dit
            # paramètre (*event.pos = event.pos[0], event.pos[1])
            # destination = Vector2D(*event.pos) - Vector2D(*sprite.get_size()) / 2.A
            #
            #
            destination = Vector2D(event.pos) - Vector2D(sprite.get_size()) / 2.
            heading = Vector2D.fromPoints(position, destination)
            heading.normalize()

    screen.blit(background, (0, 0))
    screen.blit(sprite, position)
    timePassed = clock.tick()
    timepassedSeconds = timePassed / 1000.0
    distanceMoved = timepassedSeconds * speed
    position += heading * distanceMoved
    pygame.display.update()
