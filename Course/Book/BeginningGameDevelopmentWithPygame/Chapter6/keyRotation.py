#! /usr/bin/env python3
# -*- coding:Utf8 -*-


"""ROTATION D'UNE IMAGE AVEC LES TOUCHES DE MOUVEMENT"""
"APPRESS BEGINNING GAME DEVELOPMENT - CHAPTER 6"

###########################################
#### Importation fonction et modules : ####
###########################################


import sys
sys.path.append('/home/pampi/Documents/Git/Cours-Python/Livre/BeginningGameDevelopmentWithPygame/Stock')
import pygame
from pygame.locals import *
from sys import exit
from vector2d import Vector2D
from math import sin, cos, pi


##############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####
##############################################################################

###############################
#### Programme principal : ####
###############################


back = 'Stock/sushiplate.jpg'
sprite = 'Stock/fugu.png'

pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)

background = pygame.image.load(back).convert()
sprite = pygame.image.load(sprite).convert_alpha()

clock = pygame.time.Clock()

sprite_pos = Vector2D(200, 150)
sprite_speed = 300.
sprite_rotation = 0.
sprite_rotation_speed = 360.  # Degrees per second

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    pressed_keys = pygame.key.get_pressed()

    rotation_direction = 0.
    movement_direction = 0.

    if pressed_keys[K_LEFT]:
        rotation_direction = +1.
    if pressed_keys[K_RIGHT]:
        rotation_direction = -1.
    if pressed_keys[K_UP]:
        movement_direction = +1.
    if pressed_keys[K_DOWN]:
        movement_direction = -1.

    screen.blit(background, (0, 0))

    # La rotation modifie la taille de l'image et donc réduit sa qualité
    # Il faut donc à chaque boucle modifier l'image originale
    rotated_sprite = pygame.transform.rotate(sprite, sprite_rotation)
    # Taille de la nouvelle surface ?
    w, h = rotated_sprite.get_size()
    sprite_draw_pos = Vector2D(sprite_pos.x-w/2, sprite_pos.y-h/2)
    screen.blit(rotated_sprite, sprite_draw_pos)

    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0

    sprite_rotation += rotation_direction * sprite_rotation_speed * time_passed_seconds

    # Ajustement de la nouvelle position de l'image
    # Récupération du vecteur normalisé indiquant le décalage en x et y
    heading_x = sin(sprite_rotation*pi/180.)
    heading_y = cos(sprite_rotation*pi/180.)
    heading = Vector2D(heading_x, heading_y)
    # Prise en compte du sens de rotation1
    heading *= movement_direction

    sprite_pos += heading * sprite_speed * time_passed_seconds

    pygame.display.update()
