#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""A SLIDE CASE PUZZLE"""
"MAKING GAMES WITH PYGAME : CHAPTER 4 - SLIDE PUZZLE"

"You have to find the correct position of all boxes, Have fun !!"" "

########################################
#### Classes and Methods imported : ####
########################################


import pygame
import sys
from random import choice
from pygame.locals import *
sys.path.append('/home/pampi/Documents/Git/Cours-Python/Livre/Libraries')
from pygameBase import PygameStarter


#####################
#### Constants : ####
#####################

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#######################################
#### Classes, Methods, Functions : ####
#######################################


class BaseBoard:
    """Bae class to create a board"""
    def __init__(self, display=pygame.Surface((640, 480)), size=40, gap=0,
                 nb_column=10, nb_row=7):
        self.size = size
        self.gap = gap
        self.box_color = (200, 150, 100)
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


class SlidePuzzle(BaseBoard):
    """Base class to compute slide games"""
    def __init__(self, display=pygame.Surface((640, 480)),
                 size=80, font_size=20, nb_column=4, nb_row=4):
        super().__init__(display=pygame.Surface((640, 480)),
                         size=size, gap=1, nb_column=nb_column, nb_row=nb_row)
        # Background color
        self.bg_color = (3, 54, 73)  # Dark turquoise
        # Box colors
        self.box_color = (0, 204, 0)  # Green
        self.text_color = (255, 255, 255)
        self.border_color = (100, 140, 70)

        # Board parameters
        self.size = size
        self.player_speed = int(self.size/7)
        self.computer_speed = int(self.size/2)
        self.blank = None
        self.nb_column = nb_column
        self.nb_row = nb_row
        self.board = self.start_board()

    def start_board(self):
        """Set the boxes position in the board (solving state)"""
        counter = 1
        board = []
        for x in range(self.nb_column):
            column = []
            for y in range(self.nb_row):
                column.append(counter)
                counter += self.nb_column
            board.append(column)
            counter = x + 2
        board[self.nb_column-1][self.nb_row-1] = None
        return board

    def get_blank_position(self):
        # Return the x and y of board coordinates of the blank space.
        for x in range(self.nb_column):
            for y in range(self.nb_row):
                if self.board[x][y] is None:
                    return (x, y)

    def keyboard_mouvement(self, direction):
        """Keyboard mouvement actions"""
        blank_x, blank_y = self.get_blank_position()
        if direction == LEFT:
            self.board[blank_x][blank_y], self.board[blank_x + 1][blank_y] = \
                self.board[blank_x + 1][blank_y], self.board[blank_x][blank_y]
        if direction == DOWN:
            self.board[blank_x][blank_y], self.board[blank_x][blank_y - 1] = \
                self.board[blank_x][blank_y - 1], self.board[blank_x][blank_y]
        if direction == RIGHT:
            self.board[blank_x][blank_y], self.board[blank_x - 1][blank_y] = \
                self.board[blank_x - 1][blank_y], self.board[blank_x][blank_y]
        if direction == UP:
            self.board[blank_x][blank_y], self.board[blank_x][blank_y + 1] = \
                self.board[blank_x][blank_y + 1], self.board[blank_x][blank_y]

    def valid_move(self, direction):
        """Check if the title can be push in the input direction"""
        blank_x, blank_y = self.get_blank_position()
        # Must be test
        return (direction == LEFT and blank_x != len(self.board) - 1) or \
               (direction == DOWN and blank_y != 0) or \
               (direction == RIGHT and blank_x != 0) or \
               (direction == UP and blank_y != len(self.board[0]) - 1)

    def draw_tile(self, box_x, box_y, number, font, pad_x=0, pad_y=0):
        """Draw tile on the screen
           font : This parameter must be a pygame prepared font"""

        left, top = self.left_top_coords(box_x, box_y)
        pygame.draw.rect(self.display, self.box_color, (left+pad_x, top+pad_y,
                         self.size, self.size))

        text = font.render(str(number), True, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = left + int((self.size / 2)) + pad_x, top + \
                           int((self.size / 2) + pad_y)
        self.display.blit(text, text_rect)

    def draw_board_numbered(self, font):
        """Display the board in the screen with numbered boxes
           font : This parameter must be a pygame prepared font"""
        for box_x in range(self.nb_column):
            for box_y in range(self.nb_row):
                if self.board[box_x][box_y]:  # not draw None box
                    self.draw_tile(box_x, box_y, self.board[box_x][box_y], font)

    def random_choice(self, last_move):
        """Compute a random direction"""
        directions = [LEFT, RIGHT, UP, DOWN]
        # Avoid destroy last move by removing the opposite move
        if last_move == LEFT or not self.valid_move(RIGHT):
            directions.remove(RIGHT)
        if last_move == DOWN or not self.valid_move(UP):
            directions.remove(UP)
        if last_move == UP or not self.valid_move(DOWN):
            directions.remove(DOWN)
        if last_move == RIGHT or not self.valid_move(LEFT):
            directions.remove(LEFT)
        return choice(directions)

    def new_box_place(self, direction, step=1):
        """Return the box which will move during the animation """
        blank_x, blank_y = self.get_blank_position()
        if direction == UP:
            move_x = blank_x
            move_y = blank_y + step
        elif direction == DOWN:
            move_x = blank_x
            move_y = blank_y - step
        elif direction == LEFT:
            move_x = blank_x + step
            move_y = blank_y
        elif direction == RIGHT:
            move_x = blank_x - step
            move_y = blank_y
        return (move_x, move_y, direction)


class PygameMain(PygameStarter):
    """Main program :
       Draw the board, compute start and end animations
       Control the board boxes with the mouse/keyboard"""
    def __init__(self, board, title="Slide Box Game", size=(640, 480),
                 background=(50, 60, 80)):
        super().__init__(size=size, title=title, background=background)
        self.board = board
        # Change display surface to main screen and update margins
        self.board.set_display(self.screen)
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.event_font = pygame.font.Font('freesansbold.ttf', 30)

        # Colors
        self.button_color = (0, 204, 0)
        self.buttontext_color = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.button_border_color = (100, 140, 70)
        self.button_border_highlightcolor = (200, 0, 0)

        # Buttons
        self.states = {}  # Store buttons states (motion state)
        x, y = self.board.nb_column, self.board.nb_row  # Readability
        self.reset = self.create_textbutton('  Reset puzzle  ', self.font,
                                            self.buttontext_color,
                                            self.button_color, 20,
                                            self.board.left_top_coords(x, y)[1])
        self.solve = self.create_textbutton('  Solve puzzle  ', self.font,
                                            self.buttontext_color,
                                            self.button_color, 20,
                                            self.size[1] / 2)
        self.new = self.create_textbutton('  New puzzle  ', self.font,
                                          self.buttontext_color,
                                          self.button_color, 20,
                                          self.board.left_top_coords(0, 0)[1])
        self.win = self.win()

        # Store moves to keep a trace
        self.all_moves = []
        self.reverse_solution = []

        # Create first puzzle
        self.solution = self.board.board[:]  # Puzzle solution
        self.generate_newpuzzle(80, self.board.nb_column, self.board.nb_row, 80)

    def key_up(self, key):
        """Actions when keyboard key is release"""
        mouvement = None  # Avoid UnboundLocalError when a not valid move
        if key in (K_LEFT, K_q) and self.board.valid_move(LEFT):
            mouvement = LEFT
        elif key in (K_RIGHT, K_d) and self.board.valid_move(RIGHT):
            mouvement = RIGHT
        elif key in (K_UP, K_z) and self.board.valid_move(UP):
            mouvement = UP
        elif key in (K_DOWN, K_s) and self.board.valid_move(DOWN):
            mouvement = DOWN
        if mouvement:
            self.slide_animation(mouvement, self.board.player_speed)
            self.board.keyboard_mouvement(mouvement)
            self.all_moves.append(mouvement)

    def mouse_up(self, button, pos):
        """Actions when mouse key released"""
        pos_x, pos_y = self.board.getbox_atpixel(pos[0], pos[1])
        # We check if a button was clic only if outside the board
        # Avoid useless cpu usage
        if (pos_x, pos_y) == (None, None):
            if self.reset[1].collidepoint(pos):
                self.reverse_board(self.all_moves, False)
                self.all_moves = []  # Reset moves sequence
            if self.solve[1].collidepoint(pos):
                # Except IndexError if crazy clic on Solve button
                try:
                    self.reverse_board(self.reverse_solution+self.all_moves, True)
                except IndexError:
                    pass
                self.all_moves = []
            if self.new[1].collidepoint(pos):
                self.generate_newpuzzle(80, self.board.nb_column,
                                        self.board.nb_row, 80, False)
                self.all_moves = []  # Reset moves sequence

    def mouse_motion(self, buttons, pos, rel):
        """Get mouse position and store it"""
        pos_x, pos_y = self.board.getbox_atpixel(pos[0], pos[1])
        # We check if a button was clic only if outside the board
        # Avoid useless cpu usage
        if (pos_x, pos_y) == (None, None):
            if self.reset[1].collidepoint(pos):
                self.states["Reset puzzle"] = True
            else:
                self.states["Reset puzzle"] = False
            if self.solve[1].collidepoint(pos):
                self.states["Solve puzzle"] = True
            else:
                self.states["Solve puzzle"] = False
            if self.new[1].collidepoint(pos):
                self.states["New puzzle"] = True
            else:
                self.states["New puzzle"] = False

    def draw(self):
        self.screen.fill(self.background)
        self.board.draw_board_numbered(self.font)
        self.board.draw_border()
        self.draw_button(self.reset, 'Reset puzzle')
        self.draw_button(self.solve, 'Solve puzzle')
        self.draw_button(self.new, 'New puzzle')
        if self.board.board == self.solution:
            for row in self.win:
                self.screen.blit(row[0], row[1])

    def create_textbutton(self, text, font, color, bg_color, x, y):
        """Add a text button to the screen"""
        text_surf = font.render(text, True, color, bg_color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = x, y
        self.states[text.strip()] = False  # Add button to dictionnary
        return (text_surf, text_rect)

    def draw_button(self, button, text):
        self.screen.blit(button[0], button[1])
        x, y, width, height = button[1]
        # Add effect when mouse hover the button
        if self.states[text] is True:
            pygame.draw.rect(self.screen, self.button_color,
                            (x-2, y-2, width+4, height+4), 3)
            pygame.draw.rect(self.screen, self.button_border_color,
                            (x-2, y-2, width+4, height+4), 1)
        else:
            pygame.draw.rect(self.screen, self.button_border_color,
                            (x-1, y-1, width+2, height+2), 1)

    def generate_newpuzzle(self, nb_moves=180, nb_column=5, nb_row=5, size=80,
                           animation=False):
        """Generate a new puzzle with nb_moves"""
        sequence = []  # To store a trace of all moves
        self.board = SlidePuzzle(nb_column=nb_column, nb_row=nb_row, size=80)
        self.board.set_display(self.screen)  # Use right display surface
        self.draw()
        last_move = None  # No move yet
        for i in range(nb_moves):
            self.handle_quit()
            move = self.board.random_choice(last_move)
            if animation is True:
                self.slide_animation(move, self.board.computer_speed)
                pygame.display.update()
            self.board.keyboard_mouvement(move)
            sequence.append(move)
            last_move = move
            self.draw()
        self.reverse_solution = sequence[:]

    def reverse_board(self, all_moves, animation=False):
        """Return to the start position of the board"""
        moves = all_moves[:]  # Create a copy
        moves.reverse()
        # Compute the opposite move
        for move in moves:
            if move == LEFT:
                opposite_move = RIGHT
            elif move == RIGHT:
                opposite_move = LEFT
            elif move == UP:
                opposite_move = DOWN
            elif move == DOWN:
                opposite_move = UP
            if animation is True:
                self.slide_animation(opposite_move, self.board.computer_speed)
            self.board.keyboard_mouvement(opposite_move)

    def slide_animation(self, move, animation_speed):
        """Compute a sliding animation"""
        box_x, box_y, direction = self.board.new_box_place(move)
        self.draw()
        # Create a copy of the actual screen used to display the animation
        surface = self.screen.copy()
        # Get the moving box
        left, top = self.board.left_top_coords(box_x, box_y)
        # Cover the box initial position which is currently moving
        pygame.draw.rect(surface, self.background, (left, top, self.board.size,
                                                    self.board.size))
        # Move the box to the blank position with step
        for i in range(0, self.board.size, animation_speed):
            # Animate the tile sliding over
            self.handle_quit()
            self.screen.blit(surface, (0, 0))
            if direction == UP:
                self.board.draw_tile(box_x, box_y, self.board.board[box_x][box_y],
                                     self.font, pad_y=-i)
            if direction == DOWN:
                self.board.draw_tile(box_x, box_y, self.board.board[box_x][box_y],
                                     self.font, pad_y=i)
            if direction == LEFT:
                self.board.draw_tile(box_x, box_y, self.board.board[box_x][box_y],
                                     self.font, pad_x=-i)
            if direction == RIGHT:
                self.board.draw_tile(box_x, box_y, self.board.board[box_x][box_y],
                                     self.font, pad_x=i)

            pygame.display.update()
            self.clock.tick(20)

    def win(self, text='  YOU  \n  WIN !!!  '):
        """Create the player winning animation"""
        x, y = self.board.left_top_coords(self.board.nb_column, 0)
        # Place text next to board center
        x += self.board.size
        y += self.board.size * int(self.board.nb_row/2 - 1) + self.board.size / 2
        group = []
        for ligne in text.splitlines():
            group.append(self.create_textbutton(ligne, self.event_font, self.text_color,
                                                self.background, x, y))
            y += self.board.size  # Shift to box size
        return group

########################
#### Main Program : ####
########################


if __name__ == '__main__':
    main = PygameMain(SlidePuzzle(nb_column=5, nb_row=3, size=80), size=(1100, 600))
    main.mainloop(20)
