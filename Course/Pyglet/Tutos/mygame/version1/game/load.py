#! /usr/bin/env python
# -*- coding:Utf8 -*-


########################################
#### Classes and Methods imported : ####
########################################

import pyglet
import random
import math
from functools import wraps

from game import image_resources

#####################
#### Parameters : ####
#####################


########################
#### Main Program : ####
########################


#######################################
#### Classes, Methods, Functions : ####
#######################################

def benchmark(func):
    """
        Time function
    """
    import time

    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.process_time()
        res = func(*args, **kwargs)
        print("{} has spent {} sec to finish".format(func.__name__,
                                                     time.process_time()-t))
        return res
    return wrapper


def create_asteroids(number, player_position, field_size):
    """Load <number> of asteroids"""
    for i in range(number):
        ast_x, ast_y = player_position
        while distance((ast_x, ast_y), player_position) < 100:
            ast_x = random.randint(0, field_size[0])
            ast_y = random.randint(0, field_size[1])
        new_ast = pyglet.sprite.Sprite(img=image_resources.asteroid_image,
                                       x=ast_x, y=ast_y)
        new_ast.rotation = random.randint(0, 360)
        yield new_ast


def list_asteroids(number, player_position, field_size):
    return [asteroid for asteroid in create_asteroids(number,
                                                      player_position,
                                                      field_size)]


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0]-point_2[0])**2+(point_1[1]-point_2[1])**2)


########################
#### Main Program : ####
########################
