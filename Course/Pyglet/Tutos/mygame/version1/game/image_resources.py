#! /usr/bin/env python
# -*- coding:Utf8 -*-

"""

    Prepare all resources used in the main program

"""

########################################
#### Classes and Methods imported : ####
########################################

import pyglet

#####################
#### Constants : ####
#####################

#######################################
#### Classes, Methods, Functions : ####
#######################################


def center_image(image):
    """Set an anchor point to its center"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2


########################
#### Main Program : ####
########################

# Set path from main program
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()


player_image = pyglet.resource.image("player.png")
center_image(player_image)
bullet_image = pyglet.resource.image("bullet.png")
center_image(bullet_image)
asteroid_image = pyglet.resource.image("asteroid.png")
center_image(asteroid_image)
