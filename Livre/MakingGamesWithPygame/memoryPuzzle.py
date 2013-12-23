#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""A MEMORY PUZZLE GAME"""
"MAKING GAMES WITH PYGAME : CHAPTER 3 - MEMORY PUZZLE"

"You have find all pairs on the board by using the mouse to win, Have fun !!"

###########################################
#### Importation fonction et modules : ####
###########################################

import pygame
from pygame.locals import *
import sys
from random import shuffle
sys.path.append('/home/pampi/Documents/Git/Cours-Python/Livre/Libraries')
from pygameBase import PygameStarter


#####################
#### Constants : ####
#####################

WINDOW_SIZE = (640, 480)  # Size of the window

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)

# Shapes
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

##############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####
##############################################################################


def split_into_groups(groupSize, list_in):
    """Return a generator set with list of list where groupSize is the max size"""
    # Generator
    return (list_in[i:i + groupSize] for i in range(0, len(list_in), groupSize))

    # List
    # return [list_in[i:i + groupSize] for i in range(0, len(list_in), groupSize)]

    # Set
    # return {list_in[i:i + groupSize] for i in range(0, len(list_in), groupSize)}

    # Dico
    # return {list_in[i:i + groupSize]: i for i in range(0, len(list_in), groupSize)}


class Board:
    """Base class to compute puzzle game
       len(self.colors) * len(self.shapes) * 2 >= self.nb_column * self.nb_row
       display is  the surface where the puzzle will be drawing
       <nb_column * nb_row> must be even"""
    def __init__(self, shapes, colors, display=pygame.Surface((640, 480)),
                 size=40, gap=10, nb_column=10, nb_row=7):
        self.size = size
        self.gap = gap
        self.box_color = (200, 150, 100)
        self.nb_column = nb_column
        self.nb_row = nb_row
        assert(self.nb_row * self.nb_column) % 2 == 0, 'Odd number of boxes'

        self.colors = colors
        self.shapes = shapes
        if not isinstance(self.colors, tuple) or not isinstance(self.shapes, tuple):
            raise TypeError('colors and shapes must be tuples')
        else:
            assert len(self.colors) * len(self.shapes) * 2 >= \
                self.nb_column * self.nb_row,\
                'Board too big for the actual number of colors/shapes'

        # Display and margin by default (can change it whith set_display)
        self.display = display
        self.x_margin = int((display.get_width() - (nb_column * (size + gap))) / 2)
        self.y_margin = int((display.get_height() - (nb_row * (size + gap))) / 2)

        # Fill in double the set of shapes/colors needed
        self.board = self.get_randomized()  # Board data structure
        self.states = self.generate_revealed_boxes(False)
        # Highlight Color
        self.hightlight_color = (200, 200, 200)  # Blue
        self.bg_color = (80, 80, 120)  # Navy blue

    def __repr__(self):
        """Debug"""
        return "(Board : size={}, nbCol={}, nbRow={})". \
               format(self.size, self.nb_column, self.nb_row)

    def set_display(self, display):
        """Set the diplay where the board will be draw and update margins"""
        self.display = display
        self.x_margin = int((display.get_width() - (self.nb_column *
                            (self.size + self.gap))) / 2)
        self.y_margin = int((display.get_height() - (self.nb_row *
                            (self.size + self.gap))) / 2)

    def generate_revealed_boxes(self, state):
        """Return a list of state value size of self.board"""
        return [[state] * self.nb_row for i in range(self.nb_column)]

    def get_randomized(self):
        icons = []
        for color in self.colors:
            for shape in self.shapes:
                icons.append((shape, color))
        shuffle(icons)
        nb_needed = int(self.nb_column * self.nb_row / 2)
        icons = icons[:nb_needed] * 2
        shuffle(icons)
        board = []
        for x in range(self.nb_column):
            column = []
            for y in range(self.nb_row):
                column.append(icons[0])
                del icons[0]  # Avoid an other for statement on icons size
            board.append(column)
        return board

    def getbox_atpixel(self, x, y):
        """If exist return box under x and y position, with x and y in pixel"""
        for box_x in range(self.nb_column):
            for box_y in range(self.nb_row):
                left, top = self.left_top_coords(box_x, box_y)
                box_rect = pygame.Rect(left, top, self.size, self.size)
                if box_rect.collidepoint(x, y):
                    return (box_x, box_y)
        return (None, None)  # No boxes under these coordinates

    def left_top_coords(self, box_x, box_y):
        """Take box coords and return x and y coords in pixel"""
        left = self.x_margin + (self.size + self.gap) * box_x
        top = self.y_margin + (self.size + self.gap) * box_y
        return (left, top)

    def get_shape_color(self, box_x, box_y):
        """Return shape and color at box_x and box_y coordinates"""
        #          ------ Shape ------          ------ Color ------
        return self.board[box_x][box_y][0], self.board[box_x][box_y][1]

    def draw_icons(self, shape, color, box_x, box_y):
        """Draw the shape with its color at box's pixel coordinates with
           box_x and box_y corresponding to column and row. """
        # Punish drawing out of the game space defines by nb_column and nb_row
        assert box_x < self.nb_column and box_y < self.nb_row, \
            'You try to draw out of game space : box{}'.format((box_x, box_y))

        # Add margin under the box
        quarter = int(self.size * 0.25)
        half = int(self.size * 0.5)
        # Get coords from box position
        left, top = self.left_top_coords(box_x, box_y)

        if shape == DONUT:
            pygame.draw.circle(self.display, color, (left + half, top + half),
                               half - 5)
            pygame.draw.circle(self.display, self.bg_color, (left + half, top +
                               half), quarter - 5)
        elif shape == SQUARE:
            pygame.draw.rect(self.display, color,
                            (left + quarter, top + quarter,
                             self.size - half, self.size - half))
        elif shape == DIAMOND:
            pygame.draw.polygon(self.display, color, ((left + half, top),
                               (left + self.size - 1, top + half),
                               (left + half, top + self.size - 1),
                               (left, top + half)))
        elif shape == LINES:
            pas = self.size // 10
            for i in range(0, self.size, pas):
                pygame.draw.line(self.display, color,
                                (left, top + i), (left + i, top))
                pygame.draw.line(self.display, color,
                                (left + i, top + self.size - 1),
                                (left + self.size - 1, top + i))
        elif shape == OVAL:
            pygame.draw.ellipse(self.display, color,
                               (left, top + quarter, self.size, half))

    def draw_board(self, revealed):
        """Draw the board with all shapes, covered if box not revealed"""
        for box_x in range(self.nb_column):
            for box_y in range(self.nb_row):
                left, top = self.left_top_coords(box_x, box_y)
                if not revealed[box_x][box_y]:
                    pygame.draw.rect(self.display, self.box_color,
                                    (left, top, self.size, self.size))
                else:
                    shape, color = self.get_shape_color(box_x, box_y)
                    self.draw_icons(shape, color, box_x, box_y)

    def draw_highlighted(self, box_x, box_y, color):
        """Hightlight case at box_x, box_y """
        left, top = self.left_top_coords(box_x, box_y)
        pygame.draw.rect(self.display, color,
                        (left - 5, top - 5, self.size + 10, self.size + 10), 4)


class AnimBoard(Board):
    """Add some actions to the Board class"""
    def __init__(self, shapes, colors, reveal_speed=8, size=40, gap=10,
                 nb_column=10, nb_row=7):
        super().__init__(shapes, colors, display=pygame.Surface((640, 480)),
                         size=size, gap=gap, nb_column=10, nb_row=7)
        self.reveal_speed = reveal_speed

    def reveal_box(self, boxes, clock, speed=None):
        """Reveal boxes animation
           Clock needed to see the animation (timer)"""
        if speed is None:
            speed = self.reveal_speed
           # Create an animation by drawing a rectangle smaller each iterations
           # until we can't see it (coverage < 0 (voir draw_boxcover))
        for coverage in range(self.size, (-speed) - 1, - speed):
            self.draw_boxcover(boxes, coverage, clock)

    def cover_box(self, boxes, clock, speed=None):
        """Reveal boxes animation
           Clock needed to see the animation (timer)"""
        if speed is None:
            speed = self.reveal_speed
           # Create an animation by drawing a rectangle bigger each iterations
           # until we can only see it (coverage < 0 (voir draw_boxcover))
        for coverage in range(0, self.size + speed, speed):
            self.draw_boxcover(boxes, coverage, clock)

    def draw_boxcover(self, boxes, coverage, clock):
        """pass"""
        for box in boxes:
            left, top = self.left_top_coords(box[0], box[1])
            pygame.draw.rect(self.display, self.bg_color,
                            (left, top, self.size, self.size))
            shape, color = self.get_shape_color(box[0], box[1])
            self.draw_icons(shape, color, box[0], box[1])
            if coverage > 0:  # only draw the coverage if there is an coverage
                pygame.draw.rect(self.display, self.box_color,
                                (left, top, coverage, self.size))
        pygame.display.update()
        clock.tick(25)


class PygameMain(PygameStarter):
    """Main program :
       Draw the board, compute start and end animations
       Control the board boxes with the mouse"""
    def __init__(self, board, title="Puzle Game", size=WINDOW_SIZE):
        super().__init__(size=size, title=title)
        self.board = board
        # Change display surface to main screen and update margins
        self.board.set_display(self.screen)
        # Define background colors
        self.background = self.board.bg_color  # Navy blue
        self.light_background = (235, 235, 235)  # Gray
        # Mouse position and states
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_clic = False  # No clic yet
        self.first_selection = None  # No box openned
        self.start = True  # If True compute start_animation

    def draw(self):
        self.screen.fill(self.background)
        self.board.draw_board(self.board.states)
        if self.start:
            pygame.time.wait(300)
            self.start_animation()
        self.process_actions()

    def mouse_motion(self, buttons, pos, rel):
        """Get mouse position and store it"""
        self.mouse_x, self.mouse_y = pos

    def mouse_up(self, buttons, pos):
        """Get mouse position and store it"""
        self.mouse_x, self.mouse_y = pos
        self.mouse_clic = True

    def process_actions(self):
        """Process actions if mouse on a box or if a click on box"""
        box_x, box_y = self.board.getbox_atpixel(self.mouse_x, self.mouse_y)
        if box_x is not None and box_y is not None:  # Mouse on a box
            if not self.board.states[box_x][box_y]:  # Not already discovered
                self.board.draw_highlighted(box_x, box_y,
                                            self.board.hightlight_color)
            if not self.board.states[box_x][box_y] and self.mouse_clic:
                self.board.reveal_box([(box_x, box_y)], self.clock)
                self.board.states[box_x][box_y] = True
                # Check discovered boxes
                self.selection_state(box_x, box_y)

    def selection_state(self, box_x, box_y):
        """Test if we have already discover a box"""
        if self.first_selection is None:  # Store discovered box
            self.first_selection = (box_x, box_y)
        else:  # Get shape and color for the two boxes
            ic1 = (self.board.get_shape_color(self.first_selection[0],
                                              self.first_selection[1]))
            ic2 = (self.board.get_shape_color(box_x, box_y))
            if ic1 != ic2:
                match = False
            else:
                match = True
            # Process actions according to math value
            self.do_actions(match, box_x, box_y)

    def do_actions(self, match, box_x, box_y):
        """Do actions according to match state and test if user won"""
        if match is False:
            pygame.time.wait(1000)  # pause : 1 sec
            self.board.cover_box([(self.first_selection[0],
                                 self.first_selection[1]), (box_x, box_y)],
                                 self.clock)
            self.board.states[self.first_selection[0]][self.first_selection[1]] = False
            self.board.states[box_x][box_y] = False
        if self.game_won() is True:
            self.won_animation()
            # Reset the board
            pygame.time.wait(2000)
            self.board.states = self.board.generate_revealed_boxes(False)
            self.start = True
        self.first_selection = None  # reset first_selection

    def start_animation(self):
        """Discover some box to help the player to start"""
        boxes = [[x, y] for y in range(self.board.nb_row) for x in range(self.board.nb_column)]
        shuffle(boxes)
        # Reveal slower than during the game
        for box_group in split_into_groups(10, boxes):
            self.board.reveal_box(box_group, self.clock, 6)
            pygame.time.wait(4000)
            self.board.cover_box(box_group, self.clock, 6)
        self.start = False

    def won_animation(self):
        """Highlight the board"""
        color1, color2 = self.background, self.light_background
        for i in range(10):
            # Swap colors to simulate blinking
            color1, color2 = color2, color1
            self.screen.fill(color1)
            self.board.draw_board(self.board.states)
            pygame.display.update()
            pygame.time.wait(300)

    def game_won(self):
        """Test if the player won the game"""
        # True if all True, else False
        return all(val == [True]*self.board.nb_row for val in self.board.states)

    def restart(self):
        """Set some values to start values"""
        self.mouse_clic = False

###############################
#### Programme principal : ####
###############################


main = PygameMain(AnimBoard(ALL_SHAPES, ALL_COLORS, size=30, gap=2), size=(1200, 800))
main.mainloop(10)


###########################################################
##### Test de la classe Board avec le module unittest #####
###########################################################

# if __name__ == "__main__":

    # import unittest

    # class UnitTestVector2D(unittest.TestCase):

    #     def setUp(self):
    #         pass

    #     def testCreationAndAccess(self):
    #         with self.assertRaises(TypeError):
    #             Board(ALL_SHAPES, "1")
    #         with self.assertRaises(AssertionError):
    #             Board(ALL_SHAPES, ALL_COLORS, nb_column=9)
    #         with self.assertRaises(AssertionError):
    #             Board(WHITE, ALL_SHAPES)

    #         mainBoard = Board(ALL_SHAPES, ALL_COLORS)
    #         self.assertEqual(mainBoard.left_top_coords(1, 1), (120, 115))
    #         self.assertEqual((mainBoard.x_margin, mainBoard.y_margin), (70, 65))
    #         print(".Creation and access tests passed")

    #     def testFunctions(self):
    #         mainBoard = Board(ALL_SHAPES, ALL_COLORS)
    #         test = split_into_groups(5, ALL_SHAPES)
    #         test = list(test)  # Transform generator into list
    #         self.assertEqual(len(test[0]), 5)
    #         print("Functions test passed")

    # unittest.main()

    # mainBoard = Board(ALL_SHAPES, ALL_COLORS)
    # for elem in mainBoard.board:
    #     for shape, color in elem:
    #         print(shape, color)


    # test = split_into_groups(5, ALL_SHAPES)
    # for elem in test:
    #     print(elem)
