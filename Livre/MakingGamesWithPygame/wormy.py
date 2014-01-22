#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""A SNAKE CLONE"""
"MAKING GAMES WITH PYGAME : CHAPTER 6 - WORMY"

########################################
#### Classes and Methods imported : ####
########################################

from random import randint
import pygame
from pygame.locals import *
import sys
sys.path.append('/home/pampi/Documents/Git/Cours-Python/Livre/Libraries')
from pygameBase import PygameStarter


#####################
#### Constants : ####
#####################

FPS = 30
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#######################################
#### Classes, Methods, Functions : ####
#######################################


class Snake:
    """Base class for snake entities composed of squares"""
    def __init__(self, nb_square, start_size=3):
        self._start_size = start_size  # Body width at start
        self.head = 0  # Keep snake head indice
        self.nb_square = nb_square  # Add game field limits
        self.direction = RIGHT
        self.start = self.random_position()
        self.snake = [{'x': self.start[0] - body,
                       'y': self.start[1]} for body in range(0, self.start_size, 1)]

    def random_position(self):
        """Return a random position inside the game field"""
        return (randint(5, self.nb_square[0]-2*self.start_size), randint(5, self.nb_square[1]-5))

    def _get_start_size(self):
        """Get the start_size"""
        return self._start_size

    def _set_start_size(self, value):
        """Set the start_size"""
        # Set start_size
        self._start_size = value
        # Update the snake
        self.snake = [{'x': self.start[0] - body,
                       'y': self.start[1]} for body in range(0, self.start_size, 1)]

    start_size = property(_get_start_size, _set_start_size, None, 'Update snake state with start_size')

    def move_snake(self):
        if self.direction == RIGHT:
            new_head = {'x': self.snake[self.head]['x'] + 1,
                        'y': self.snake[self.head]['y']}
        elif self.direction == LEFT:
            new_head = {'x': self.snake[self.head]['x'] - 1,
                        'y': self.snake[self.head]['y']}
        elif self.direction == UP:
            new_head = {'x': self.snake[self.head]['x'],
                        'y': self.snake[self.head]['y'] - 1}
        elif self.direction == DOWN:
            new_head = {'x': self.snake[self.head]['x'],
                        'y': self.snake[self.head]['y'] + 1}
        self.snake.insert(0, new_head)

    def add_food(self):
        """Add food to a random location"""
        self.food = {'x': randint(0, self.nb_square[0] - 1),
                     'y': randint(0, self.nb_square[1] - 1)}

    def check_state(self):
        """Check if the snake ate himself or if he hit the game field limits"""

        # Check if the snake go out the game limits
        if self.snake[self.head]['x'] == -1 or \
           self.snake[self.head]['x'] == self.nb_square[0] or \
           self.snake[self.head]['y'] == -1 or \
           self.snake[self.head]['y'] == self.nb_square[1]:
                return 'game over'  # Snake out of game field

        # Check if the snake eats himself
        for body in self.snake[1:]:  # Except self.head
            if (body['x'], body['y']) == (self.snake[self.head]['x'], self.snake[self.head]['y']):
                return 'game over'  # Snake eats himself

    def has_eat(self):
        """Check if the snake ate an apple"""
        if self.snake[self.head]['x'] == self.food['x'] and \
           self.snake[self.head]['y'] == self.food['y']:
            return True
        else:
            return False


class PygameMain(PygameStarter):
    """Main program :
       Draw the grid, compute start and end animations
       Control the board boxes with the mouse/keyboard"""
    def __init__(self, title="WORM OR SNAKE ?", size=(640, 480), cell_size=20,
                 background=(60, 60, 60)):
        super().__init__(size=size, title=title, background=background)
        # Cells parameters
        self.cell_size = cell_size
        self.cell_dimension = (int(self.size[0]/self.cell_size),
                               int(self.size[1]/self.cell_size))
        assert self.size[0] % self.cell_size == 0, "You must choice a cell size as a multiple of screen width"
        assert self.size[1] % self.cell_size == 0, "You must choice a cell size as a multiple of screen height"

        # Grid color
        self.grid_color = (80, 80, 80)

        # Prepare font
        self.font = pygame.font.Font('freesansbold.ttf', 18)

        # Add Snake

    def draw_grid(self):
        """Draw the background grid"""
        for x in range(0, self.size[0], self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.size[1]))
        for y in range(0, self.size[1], self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.size[0], y))

    def draw_apple(self):
        """Draw an apple ina random position"""
        pass

    def draw(self):
        self.draw_grid()


########################
#### Main Program : ####
########################


if __name__ == '__main__':

    worm = Snake((20, 10))
    print(worm.start_size, worm.snake)
    worm.start_size = 5
    print(worm.start_size, worm.snake)
    worm.move_snake()
    print(worm.snake, worm.start_size)
    main = PygameMain(cell_size=20)
    main.mainloop(FPS)
