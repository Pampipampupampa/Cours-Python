#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""A MEMORIZE GAME"""
"MAKING GAMES WITH PYGAME : CHAPTER 5 - SIMULATE"""

"You have to try to find the correct order after computer demo, Have fun !! "

########################################
#### Classes and Methods imported : ####
########################################


import pygame
from random import choice, randint
import time
import sys
from pygame.locals import *
sys.path.append('/home/pampi/Documents/Git/Cours-Python/Livre/Libraries')
from pygameBase import PygameStarter


#####################
#### Constants : ####
#####################


# If you want to make the game harder add color and change the board size
# according to colors numbers
# You must have an even number of colors and highlight_colors
# Number of color and number of boxes must be equal

COLORS = {'red': (155, 0, 0),
          'green': (0, 155, 0),
          'blue': (0, 0, 155),
          'yellow': (155, 155, 0),
          'cyan': (16, 122, 107),
          'orange': (151, 89, 17)}

HIGHLIGHT_COLORS = {'red': (255, 0, 0),
                    'green': (0, 255, 0),
                    'blue': (0, 0, 255),
                    'yellow': (255, 255, 0),
                    'cyan': (116, 222, 207),
                    'orange': (251, 189, 117)}
PATH = "Stock/"

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
        self.border_color = (100, 150, 100)
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


class Simulate(BaseBoard):
    """Main class to compute the game"""
    def __init__(self, colors, highlight_colors,
                 display=pygame.Surface((640, 480)), size=180,
                 font_size=20, nb_column=2, nb_row=2):
        super().__init__(display=pygame.Surface((640, 480)),
                         size=size, gap=20, nb_column=nb_column, nb_row=nb_row)
        self.box_color = colors
        self.boxhightlighted_color = highlight_colors
        assert len(COLORS) == len(HIGHLIGHT_COLORS), \
            'You must have even COLORS and highlight_colors'
        assert len(COLORS) == nb_column*nb_row, \
            'You must have even number of color and boxes'
        # Store in dico color and rect to later draw all boxes
        self.rect_dico = {}

    def create_board(self):
        """Create a dico with color and rectangle informations for all boxes"""
        dico = {}
        color = [color for color in self.box_color]
        i = 0
        for box_x in range(self.nb_column):
            for box_y in range(self.nb_row):
                left, top = self.left_top_coords(box_x, box_y)
                elem = '{}Rect'.format(color[i])
                dico[elem] = (self.box_color[color[i]], pygame.Rect(left, top,
                                                                    self.size,
                                                                    self.size))
                i += 1
        return dico

    def draw_tile(self, pad_x=0, pad_y=0):
        """Draw boxes on the screen"""
        for rect in self.rect_dico:
            pygame.draw.rect(self.display, self.rect_dico[rect][0],
                             self.rect_dico[rect][1])


class PygameMain(PygameStarter):
    """Main program :
       Draw the board, compute start and end animations
       Control the board boxes with the mouse/keyboard"""
    def __init__(self, board, title="Simulate", size=(640, 480),
                 background=(60, 60, 60)):
        super().__init__(size=size, title=title, background=background)
        self.board = board
        # Change display surface to main screen and update margins
        self.board.set_display(self.screen)
        self.board.rect_dico = self.board.create_board()
        # Add changing background color (keep self.background as initial value)
        self.changed_background = self.background
        # Add a font to display text on screen
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        # Prepare sounds
        self.beeps = [pygame.mixer.Sound(PATH+'beep1.ogg'),
                      pygame.mixer.Sound(PATH+'beep2.ogg'),
                      pygame.mixer.Sound(PATH+'beep3.ogg'),
                      pygame.mixer.Sound(PATH+'beep4.ogg')]

        self.pattern = []  # Store all steps
        self.step = 0  # Next pattern box index to push
        # Prepare help
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.info = self.prepare_text('Match the pattern by clicking boxes ' +
                                      'in the right order', self.font,
                                      (200, 200, 200), self.background,
                                      10, self.size[1]-25)
        # Prepare score
        self.score = 0
        self.score_text = self.prepare_text('Score :  0',
                                            self.font, (200, 200, 200),
                                            self.background,
                                            self.size[0]-100, 10)
        # Initialize mouse state
        self.mouse_clic = False
        self.clicked_button = None

        # Needed to block computer animation and to let the player play
        self.start_demo = True  # True means computer turn

        # Need time to know when the player is waiting too much
        self.last_click = 0
        self.timeout = 4  # Max time between clicks

        # Display board before start
        self.draw()
        pygame.display.flip()

    def draw(self):
        self.board.draw_tile()
        self.screen.blit(self.info[0], self.info[1])
        self.screen.blit(self.score_text[0], self.score_text[1])

    def update(self):
        """Choose if it's computer or player turn"""
        if self.start_demo:
            self.computer_turn()
        else:
            self.player_turn()
        self.score_text = self.prepare_text('Score :  ' + str(self.score),
                                            self.font, (200, 200, 200),
                                            self.changed_background,
                                            self.size[0]-100, 10)

    def mouse_up(self, button, pos):
        """Return the rectangle boxe coordinates at mouse clic"""
        for color, rect in self.board.rect_dico.items():
            if rect[1].collidepoint((pos)):
                self.clicked_button = color  # Recup box name
                return

    def restart(self):
        """Set some values to start values each end of the loop"""
        self.mouse_clic = False
        self.clicked_button = None

    def prepare_text(self, text, font, color, bg_color, x, y):
        """Prepare a text to be blit to the screen"""
        text_surf = font.render(text, True, color, bg_color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = x, y
        return (text_surf, text_rect)

    def clic_animation(self, rect_color, speed=50):
        """Add flash when player clic on a box"""
        flash_color = self.board.boxhightlighted_color[rect_color[:-4]]
        rect = self.board.rect_dico[rect_color][1]
        flash_surf = pygame.Surface((self.board.size, self.board.size)).convert_alpha()
        origin_surf = self.screen.copy()
        # Recup each color to add alpha later
        r, g, b = flash_color
        # Play random sound to confuse the player, mouahahaha !!
        choice(self.beeps).play()
        # Animation loop (flash_surf more and more visible then the opposite)
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, speed*step):
                self.handle_quit()
                # Start animation
                flash_surf.fill((r, g, b, alpha))
                self.screen.blit(origin_surf, (0, 0))
                self.screen.blit(flash_surf, rect.topleft)
                pygame.display.update()
                self.clock.tick(20)
        self.screen.blit(origin_surf, (0, 0))

    def game_over(self, speed=50):
        """Do game over animation"""
        origin_surf = self.screen.copy()
        flash_surf = pygame.Surface(self.screen.get_size())
        flash_surf = flash_surf.convert_alpha()
        r, g, b = (255, 255, 255)  # White color animation
        # Play all sounds
        for beep in self.beeps:
            beep.play()
        for i in range(3):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, speed*step):
                    self.handle_quit()
                    flash_surf.fill((r, g, b, alpha))
                    # Flash animation
                    self.screen.blit(origin_surf, (0, 0))
                    self.screen.blit(flash_surf, (0, 0))
                    self.draw()  # Redraw other surfaces
                    pygame.display.update()
                    self.clock.tick(20)

    def computer_turn(self):
        """Do the computer animation"""
        pygame.time.wait(500)
        self.pattern.append(choice(list(self.board.rect_dico)))
        for rect_color in self.pattern:
            self.clic_animation(rect_color)
            pygame.time.wait(500)
        self.start_demo = False

    def player_turn(self):
        """Let the player do actions"""
        if self.clicked_button and self.clicked_button == self.pattern[self.step]:
            self.clic_animation(self.clicked_button)
            self.step += 1  # Navigate inside the pattern
            self.last_click = time.time()  # Store current time
            if self.step == len(self.pattern):
                self.change_background()
                self.score += 1
                self.step = 0  # Reset step
                self.start_demo = True
                pygame.time.wait(1000)
        # Wrong box
        elif self.clicked_button and self.clicked_button != self.pattern[self.step]:
            self.lose_actions()
        # Too late
        elif self.step != 0 and time.time() - self.timeout > self.last_click:
            self.lose_actions()

    def lose_actions(self):
        """Do some actions when the player lose"""
        self.game_over()
        self.pattern = []
        self.step = 0
        self.score = 0
        pygame.time.wait(1000)
        self.start_demo = True
        self.change_background(self.background)

    def change_background(self, color=None):
        """Change background color"""
        # Allow to choose the background color (like default background color)
        if color:
            self.changed_background = color
        else:
            self.changed_background = (randint(0, 255),
                                       randint(0, 255),
                                       randint(0, 255))
        background = pygame.Surface(self.screen.get_size())
        background.fill(self.changed_background)
        self.screen.blit(background, (0, 0))

########################
#### Main Program : ####
########################

if __name__ == '__main__':
    main = PygameMain(Simulate(colors=COLORS, highlight_colors=HIGHLIGHT_COLORS,
                      nb_column=3, nb_row=2), size=(750, 600))
    main.mainloop(20)
