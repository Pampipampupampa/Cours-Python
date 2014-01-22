#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""A MEMORY PUZZLE GAME"""
"MAKING GAMES WITH PYGAME : CHAPTER 3 - MEMORY PUZZLE"

"You have find all pairs on the board by using the mouse to win, Have fun !!"

########################################
#### Classes and Methods imported : ####
########################################

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
PINK = (150, 40, 80)
LIGHT_GREEN = (170, 190, 140)
ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN, PINK, LIGHT_GREEN)

# Shapes
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
DOUBLE_SQUARE = 'double_square'
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL, DOUBLE_SQUARE)

# Pictures
CAT = 'cat.png'
GEM = 'gem1.png'
PINK_GIRL = 'pinkgirl.png'
ALL_PICTURES = (CAT, GEM, PINK_GIRL)

#######################################
#### Classes, Methods, Functions : ####
#######################################


def split_into_groups(groupSize, list_in):
    """Return a generator compute with list of list where groupSize is the max size"""
    # Generator
    return (list_in[i:i + groupSize] for i in range(0, len(list_in), groupSize))

    # List
    # return [list_in[i:i + groupSize] for i in range(0, len(list_in), groupSize)]

    # Set
    # return {list_in[i:i + groupSize] for i in range(0, len(list_in), groupSize)}

    # Dico
    # return {list_in[i:i + groupSize]: i for i in range(0, len(list_in), groupSize)}


class BaseBoard:
    """Bae class to create a board"""
    def __init__(self, display=pygame.Surface((640, 480)), size=40, gap=0,
                 nb_column=10, nb_row=7):
        self.size = size
        self.gap = gap
        self.box_color = (200, 150, 100)
        self.border_color = (255, 255, 255)
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

    def draw_border(self, thick=4):
        """Add a border to delimit the game"""
        left, top = self.left_top_coords(0, 0)
        width = (self.size + self.gap) * self.nb_column
        height = (self.size + self.gap) * self.nb_row
        pygame.draw.rect(self.display, self.border_color,
                        (left-thick+1, top-thick+1, width+thick, height+thick),
                         thick)

class EvenPuzzle(BaseBoard):
    """Base class to compute puzzle game

       Steps after initialize :
       Change display surface to main screen with <set_display>.
       Set the picture dictionnary with <set_picture_dico>.
       Initialize the board with <get_randomized>.

    """
    def __init__(self, shapes, colors, pictures=None, display=pygame.Surface((640, 480)),
                 size=40, gap=10, nb_column=10, nb_row=7):
        super().__init__(display=pygame.Surface((640, 480)),
                         size=size, gap=gap, nb_column=nb_column, nb_row=nb_row)
        self.size = size
        self.gap = gap
        self.box_color = (200, 150, 100)
        self.nb_column = nb_column
        self.nb_row = nb_row
        assert(self.nb_row * self.nb_column) % 2 == 0, 'Odd number of boxes'

        self.colors = colors
        self.shapes = shapes
        self.pictures = pictures
        # Control input type
        if self.pictures and not isinstance(self.pictures, tuple):
            raise TypeError('Pictures must be tuples')
        elif not isinstance(self.colors, tuple):
            raise TypeError('Colors must be tuples')
        elif not isinstance(self.shapes, tuple):
            raise TypeError('Shapes must be tuples')

        # Control if we have enough elements to display
        if self.pictures:
            assert (len(self.colors) * len(self.shapes)*2 + len(self.pictures)*2) >= \
                self.nb_column * self.nb_row,\
                'Board too big for the actual number of colors/shapes, pictures'
        else:
            assert (len(self.colors) * len(self.shapes)*2) >= \
                self.nb_column * self.nb_row,\
                'Board too big for the actual number of colors/shapes, pictures'

        # Fill in double the set of shapes/colors needed
        self.board = []  # Board data structure
        self.states = self.generate_revealed_boxes(False)  # All covered
        # Background color
        self.bg_color = (80, 80, 120)  # Navy blue
        # Highlight color
        self.hightlight_color = (200, 200, 200)  # Gray

    def set_picture_dico(self, pictures):
        """Create a dico with pictures images to load them only once
           Pictures are load, rescale, and then added"""
        dico = {}
        for picture in pictures:
            image = pygame.image.load("Stock/" + picture).convert_alpha()
            image = pygame.transform.scale(image, (self.size, self.size))
            dico[picture] = image
        return dico

    def generate_revealed_boxes(self, state):
        """Return a list of state value size of self.board"""
        return [[state] * self.nb_row for i in range(self.nb_column)]

    def get_randomized(self):
        icons = []
        for color in self.colors:
            for shape in self.shapes:
                icons.append((shape, color))
        shuffle(icons)
        if self.pictures:  # Only if we have pictures
            for picture in self.pictures:
                icons.append((picture, self.colors[0]))
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
        elif shape == DOUBLE_SQUARE:
            pygame.draw.rect(self.display, color, (left + quarter, top,
                             half, quarter))
            pygame.draw.rect(self.display, color, (left + quarter,
                             top + (half+quarter), self.size - half,
                             quarter))
        else:  # Display pictures
            self.display.blit(self.dico_picture[shape], (left, top))

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

    def draw_border(self):
        """Add a border to delimit the game"""
        left, top = self.left_top_coords(0, 0)
        width = (self.size + self.gap) * self.nb_column
        height = (self.size + self.gap) * self.nb_row
        pad = 0.1*self.x_margin
        pygame.draw.rect(self.display, self.border_color,
                        (left - pad, top - pad, width + pad,
                         height + pad), 4)


class AnimEvenPuzzle(EvenPuzzle):
    """Add some actions to Board class
       ---> Sliding door animation on cover and reveal
    """
    def __init__(self, shapes, colors, pictures=None, reveal_speed=8, size=40, gap=10,
                 nb_column=10, nb_row=7):
        super().__init__(shapes, colors, pictures, display=pygame.Surface((640, 480)),
                         size=size, gap=gap, nb_column=nb_column, nb_row=nb_row)
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
        """Cover boxes animation
           Clock needed to see the animation (timer)"""
        if speed is None:
            speed = self.reveal_speed
           # Create an animation by drawing a rectangle bigger each iterations
           # until we can only see it (coverage < 0 (voir draw_boxcover))
        for coverage in range(0, self.size + speed, speed):
            self.draw_boxcover(boxes, coverage, clock)

    def draw_boxcover(self, boxes, coverage, clock):
        for box in boxes:
            left, top = self.left_top_coords(box[0], box[1])
            pygame.draw.rect(self.display, self.bg_color,
                            (left, top, self.size, self.size))
            shape, color = self.get_shape_color(box[0], box[1])
            self.draw_icons(shape, color, box[0], box[1])
            if coverage > 0:  # only draw the coverage if there is an coverage
                pygame.draw.rect(self.display, self.box_color,
                                (left, top, min(coverage, self.size), self.size))
        pygame.display.update()
        clock.tick(20)


class PygameMain(PygameStarter):
    """Main program :
       Draw the board, compute start and end animations
       Control the board boxes with the mouse"""
    def __init__(self, board, title="Puzle Game", size=WINDOW_SIZE):
        super().__init__(size=size, title=title)
        self.board = board
        # Change display surface to main screen and update margins
        self.board.set_display(self.screen)
        # Load pictures and adapt scales to boxes, then store them in dico
        self.board.dico_picture = self.board.set_picture_dico(self.board.pictures)
        # Initialize the board
        self.board.board = self.board.get_randomized()

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
        self.board.draw_border()
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
            pygame.time.wait(3000)
            self.board.states = self.board.generate_revealed_boxes(False)
            self.start = True
        self.first_selection = None  # reset first_selection

    def start_animation(self):
        """Discover some box to help the player to start"""
        boxes = [[x, y] for y in range(self.board.nb_row) for x in range(self.board.nb_column)]
        shuffle(boxes)
        # Reveal slower than during the game
        for box_group in split_into_groups(8, boxes):
            self.board.reveal_box(box_group, self.clock)
            self.handle_quit()  # Add quit event if user want to quit now
            pygame.time.wait(500)
            self.board.cover_box(box_group, self.clock)
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


########################
#### Main Program : ####
########################


if __name__ == '__main__':
    main = PygameMain(AnimEvenPuzzle(ALL_SHAPES, ALL_COLORS, ALL_PICTURES, size=50,
                      gap=10, nb_column=12, nb_row=8), size=(1000, 600))
    main.mainloop(20)


#########################################
##### Test EvenPuzzle with unittest #####
#########################################

# if __name__ == "__main__":

    # import unittest

    # class UnitTestVector2D(unittest.TestCase):

    #     def setUp(self):
    #         pass

    #     def testCreationAndAccess(self):
    #         with self.assertRaises(TypeError):
    #             EvenPuzzle(ALL_SHAPES, "1")
    #         with self.assertRaises(AssertionError):
    #             EvenPuzzle(ALL_SHAPES, ALL_COLORS, nb_column=9)
    #         with self.assertRaises(AssertionError):
    #             EvenPuzzle(WHITE, ALL_SHAPES)

    #         mainBoard = EvenPuzzle(ALL_SHAPES, ALL_COLORS)
    #         self.assertEqual(mainBoard.left_top_coords(1, 1), (120, 115))
    #         self.assertEqual((mainBoard.x_margin, mainBoard.y_margin), (70, 65))
    #         print(".Creation and access tests passed")

    #     def testFunctions(self):
    #         mainBoard = EvenPuzzle(ALL_SHAPES, ALL_COLORS)
    #         test = split_into_groups(5, ALL_SHAPES)
    #         test = list(test)  # Transform generator into list
    #         self.assertEqual(len(test[0]), 5)
    #         print("Functions test passed")

    # unittest.main()

    # mainBoard = EvenPuzzle(ALL_SHAPES, ALL_COLORS)
    # for elem in mainBoard.board:
    #     for shape, color in elem:
    #         print(shape, color)


    # test = split_into_groups(5, ALL_SHAPES)
    # for elem in test:
    #     print(elem)
