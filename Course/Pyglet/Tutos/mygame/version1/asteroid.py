#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""First part of asteroid game"""
"http://steveasleep.com/pyglettutorial.html#intro"

########################################
#### Classes and Methods imported : ####
########################################

import pyglet
from game import image_resources as img_src
from game import load


######################
#### Parameters : ####
######################

# Set up windows
# game_win1 = pyglet.window.Window(800, 600)

# Set up two label
score_label = pyglet.text.Label(text="Score : 0", x=10, y=575)
level_label = pyglet.text.Label(text="Version 1: Static Graphics",
                                x=400, y=575, anchor_x="center")

# Set player sprite
player_ship = pyglet.sprite.Sprite(img=img_src.player_image, x=400, y=300)


#######################################
#### Classes, Methods, Functions : ####
#######################################

# Two methods to change Windows display : Inherite class or decorator

class MainWindow(pyglet.window.Window):
    """docstring for MainWindow"""
    def __init__(self, width, height):
        super().__init__(width=width, height=height)

    def on_draw(self):
        """Decorator used to tell him : it's an event handler"""
        self.clear()
        score_label.draw()
        level_label.draw()
        player_ship.draw()
        for asteroid in asteroids:
            asteroid.draw()


# @game_win1.event
# def on_draw():
#     """Decorator used to tell him : it's an event handler"""
#     game_win1.clear()
#     score_label.draw()
#     level_label.draw()
#     player_ship.draw()
#     for asteroid in asteroids:
#         asteroid.draw()


########################
#### Main Program : ####
########################

# Set the main window
game_win = MainWindow(800, 600)
asteroids = load.create_asteroids(4, player_ship.position, game_win.get_size())


if __name__ == '__main__':
    pyglet.app.run()
