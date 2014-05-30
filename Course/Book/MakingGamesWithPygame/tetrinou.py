# ! /usr/bin/env python
# -*- coding:Utf8 -*-


"""A TETRIS CLONE"""
"MAKING GAMES WITH PYGAME : CHAPTER 7 - TETRINOU"

########################################
#### Classes and Methods imported : ####
########################################

import random
import pygame
from pygame.locals import *

from sys import path
path.append('/home/pampi/Documents/Git/Cours-Python/Library')
from pygameBase import PygameStarter

#####################
#### Constants : ####
#####################

SCREEN_SIZE = (1200, 900)
FPS = 10

#######################################
#### Classes, Methods, Functions : ####
#######################################


class BaseBoard:
    """Base class to create a board"""
    def __init__(self, display=pygame.Surface((640, 480)), size=40, gap=0,
                 nb_column=10, nb_row=7):
        self.size = size
        self.gap = gap
        self.box_color = (200, 150, 100)
        self.border_color = (200, 150, 100)
        self.nb_column = nb_column
        self.nb_row = nb_row

        # Display and margin by default (can change it whith set_display)
        self.display = display
        self.x_margin = int((display.get_width() - (nb_column * (size + gap))) / 2)
        self.y_margin = int((display.get_height() - (nb_row * (size + gap))) / 2)

    def __repr__(self):
        """Debug display"""
        return "(Board : size={}, nbCol={}, nbRow={})". \
               format(self.size, self.nb_column, self.nb_row)

    def set_display(self, display):
        """Set the diplay where the board will be draw and update margins"""
        self.display = display
        self.x_margin = int((display.get_width() - (self.nb_column *
                            (self.size + self.gap))) / 2)
        self.y_margin = int((display.get_height() - (self.nb_row *
                            (self.size + self.gap))) / 2)

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

    def draw_border(self, thick=2):
        """Add a border to delimit the game"""
        left, top = self.left_top_coords(0, 0)
        width = (self.size + self.gap) * self.nb_column
        height = (self.size + self.gap) * self.nb_row
        pygame.draw.rect(self.display, self.border_color,
                        (left-thick/2, top-thick/2, width+thick, height+thick),
                         thick)


class TetrinouSandbox(BaseBoard):
    """Creation of the main game scene"""

    BLANK = "."  # Text character used to define a blank space in the board

    def __init__(self, size=20, nb_column=20, nb_row=30,
                 bg_color=(230, 200, 150), border_color=(70, 50, 30)):
        super().__init__(size=size, nb_column=nb_column, nb_row=nb_row)
        self.size = size
        self.nb_column = nb_column
        self.nb_row = nb_row
        self.board = self.generate_blank_board
        self.bg_color = bg_color
        self.border_color = border_color
        assert(self.nb_row * self.nb_column) % 2 == 0, 'Odd number of boxes'

    @property
    def generate_blank_board(self):
        """Return a list of list of blanks values"""
        return [[self.BLANK] * self.nb_row for i in range(self.nb_column)]

    def on_board(self, x, y):
        """Check if (x, y) are on board or outside"""
        return x >= 0 and x < self.nb_column and y < self.nb_row

    def valid_position(self, piece, add_x, add_y):
        """Check if next piece position is a valid position
           add_x and add_y are used to move piece to left, right, or bottom"""
        for x in piece.TEMPLATE_WIDTH:
            for y in piece.TEMPLATE_HEIGHT:
                # Check if the piece's box is above the board or an empty space
                # and move on to the next iteration
                is_above = y + piece.y + add_y < 0
                is_empty = piece.shapes[piece.shape][piece.rotation][x][y] == self.BLANK
                if is_empty or is_above:
                    continue
                # Test if a not blank box are outside the board
                if not self.on_board(x + piece.x + add_x, y + piece.y + add_y):
                    return False
                # Test if piece box is not colliding with a board box
                if board[x + piece.x + add_x][y + piece.y + add_y] != self.BLANK:
                    return False
        return True

    def complete_line(self, row):
        """Check if a row hasn't blank space on it"""
        for column in range(self.nb_column):
            if self.board[row][column] == self.BLANK:
                return False
        return True

    @property
    def remove_lines(self):
        """Remove all complete lines and move everything above them down
           Return how many lines are deleted"""
        removed_lines = 0
        y = self.nb_row - 1  # Start algo on the bottom
        while y >= 0:
            if complete_line(y):
                for old_y in range(y, 0, -1):
                    for x in range(self.nb_column):
                        # Duplicate row above to row down
                        self.board[x][old_y] = self.board[x][old_y-1]
                # Remove the hightest row
                for x in range(self.nb_column):
                    self.board[x][0] = BLANK
                removed_lines += 1  # Add 1 for each deleted rows
            # If a row is deleted <y> isn't incremented so we can check if the
            # new row is also completed
            else:
                y -= 1
        return removed_lines

    def draw_box(self, box_x, box_y, color, pos_x=None, pos_y=None):
        """
            Draw a single box at input coordinates

            Accept specific coordinates with x and y parameters

            If pos_x and pos_y are None the function will use box_x and box_y
            to get specific coordinates
        """
        # Empty space draw nothing (used with draw_board method)
        if color == self.BLANK:
            return
        if pos_x is None and pos_y is None:
            pos_x, pos_y = getbox_atpixel(box_x, box_y)
        pygame.draw.rect(self.display, Piece.COLORS[color], (pos_x+1, pos_y+1,
                         self.size-1, self.size-1))
        # Add a shadow on the box bottom right side
        pygame.draw.rect(self.display, Piece.LIGHT_COLORS[color], (pos_x+1,
                         pos_y+1, self.size-4, self.size-4))

    @property
    def draw_board(self):
        """Draw board background and all boxes on the board"""
        pygame.draw.rect(self.display, self.bg_color,
                        (self.x_margin, self.y_margin,
                         self.nb_column*self.size, self.nb_row*self.size))
        for x in range(self.nb_column):
            for y in range(self.nb_row):
                self.draw_box(x, y, self.board[x][y])


class Shape(object):
    """Load shapes files and store them"""

    TEMPLATE_WIDTH = 5
    TEMPLATE_HEIGHT = 5
    FILES = ("Z.csv", "L.csv", "J.csv", "I.csv", "O.csv", "T.csv", "U.csv")

    # Keeps all shapes as a class attribute
    shapes = {}

    def __init__(self, path=""):
        self.path = path

    def load(self, source, delimiter=' '):
        """Load the shapes templates from a text file"""
        with open(source, 'r') as f:
            # Remove leading, trailing and delimiting characters
            clean_file = f.read().strip().replace(delimiter, '')
            # Get only file name
            name = f.name.split('.')[0][len(self.path):]
            print(name)
            # Return name and shape templates
            return name, [row.split('\n') for row in clean_file.split('\n#\n')]

    def store(self, files=FILES):
        """Store in shapes all shapes in files.
           files ---> must be tuple of each source file name"""
        for source in files:
            name, shape = self.load(self.path+source)
            self.shapes[name] = shape

    def state(self):
        """Change shape states"""
        pass


class Piece(Shape):
    """Class used to create a new random piece on the board"""

    COLORS = {'red': (155, 0, 0),
              'green': (0, 155, 0),
              'blue': (0, 0, 155),
              'yellow': (155, 155, 0),
              'cyan': (16, 122, 107),
              'orange': (151, 89, 17)}

    LIGHT_COLORS = {'red': (255, 0, 0),
                    'green': (0, 255, 0),
                    'blue': (0, 0, 255),
                    'yellow': (255,  255, 0),
                    'cyan': (116, 222, 207),
                    'orange': (251, 189, 117)}

    def __init__(self, board, path):
        super().__init__(path=path)
        self.board = board
        self.store()
        self.random_piece

    @property
    def random_piece(self):
        """Create a new piece with random shape and parameters"""
        self.shape = random.choice(list(self.shapes))
        self.rotation = random.randint(0, len(self.shapes[self.shape]) - 1)
        self.color = random.choice(list(self.COLORS))
        self.x = int(self.board.nb_column / 2) - int(self.TEMPLATE_WIDTH / 2)
        self.y = -2  # Start above the board to let player prepare itself

    def draw_piece(self, pos_x=None, pos_y=None):
        if pos_x is None and pos_y is None:
            pos_x, pos_y = self.board.left_top_coords(self.x, self.y)
        for x in range(self.TEMPLATE_WIDTH):
            for y in range(self.TEMPLATE_HEIGHT):
                if self.shapes[self.shape][self.rotation][x][y] != self.board.BLANK:
                    self.board.draw_box(None, None, self.color,
                                        pos_x + x*(self.board.size +
                                                   self.board.gap),
                                        pos_y + y*(self.board.size +
                                                   self.board.gap))


class MainScreen(PygameStarter):
    """Main program with the game mainloop"""
    def __init__(self, size, title="TETRINOU !!", background=(130, 100, 75)):
        super().__init__(title=title, size=size, background=background)
        self.board = TetrinouSandbox(size=25)
        self.board.set_display(self.screen)
        # Print test
        self.first_shape = Piece(self.board, "Stock/")

    def draw(self):
        # Just to test
        self.board.draw_board
        self.board.draw_border()
        # self.first_shape.draw_piece()
        # self.first_shape.draw_piece(600, 600)
        Piece(self.board, "Stock/").draw_piece(500, 400)

    def draw_next_piece(self):
        """Draw how the next piece looks like"""
        pass


########################
#### Main Program : ####
########################

if __name__ == '__main__':

    # Test MainScreen creation
    MainScreen(SCREEN_SIZE).mainloop(FPS)

    # Test Shape class : Try to load every shapes
    # forme = Shape("Stock/")
    # forme.store()
    # print(Shape.shapes, "\n")
    # for el in Shape.shapes:
    #     for val in Shape.shapes[el]:
    #         for row in range(len(val)):
    #             print(val[row], '\n')
    #         print('\n')

    # Test board creation and piece creation
    # board = TetrinouSandbox()
    # print(len(board.board), len(board.board[0]))
    # piece = Piece(board, "Stock/")
    # print(piece.shape, piece.rotation, piece.color, piece.x, piece.y)
