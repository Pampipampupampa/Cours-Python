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
sys.path.append('/home/pampi/Documents/Git/Cours-Python/Library')
from pygameBase import PygameStarter


#####################
#### Constants : ####
#####################

SCREEN_SIZE = (1200, 800)
FPS = 10
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#######################################
#### Classes, Methods, Functions : ####
#######################################


class Snake:
    """Base class for snake entities composed of squares
       nb_square must contains numbers of square by length and width
       length let you choose the initial snake length"""
    def __init__(self, nb_square, length=3):
        self._length = length  # Body length at start
        self.head = 0  # Keep snake head indice
        self.nb_square = nb_square  # Add game field limits
        self.direction = RIGHT
        self.start = self.random_position
        self.snake = [{'x': self.start[0] - body,
                       'y': self.start[1]} for body in range(0, length, 1)]
        self.add_food()

    @property
    def random_position(self):
        """Return a random position inside the game field"""
        return (randint(5, self.nb_square[0]-2),
                randint(5, self.nb_square[1]-5))

    def _get_length(self):
        """Get the length"""
        return self._length

    def _set_length(self, value):
        """Set the length"""
        # Update the snake
        self.snake = [{'x': self.start[0] - body,
                       'y': self.start[1]} for body in range(0, value, 1)]
        # Set length
        self._length = value

    length = property(_get_length, _set_length, None,
                      'Update snake state with length')

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

    def game_over(self):
        """Check if the snake ate himself or if he hit the game field limits"""

        # Check if the snake go out the game limits
        if self.snake[self.head]['x'] == -1 or \
           self.snake[self.head]['x'] == self.nb_square[0] or \
           self.snake[self.head]['y'] == -1 or \
           self.snake[self.head]['y'] == self.nb_square[1]:
                return True  # Snake out of game field

        # Check if the snake eats himself
        for body in self.snake[1:]:  # Except self.head
            if (body['x'], body['y']) == (self.snake[self.head]['x'],
                                          self.snake[self.head]['y']):
                return True  # Snake eats himself
        return False

    def has_eat(self):
        """Check if the snake ate an apple"""
        if self.snake[self.head]['x'] == self.food['x'] and \
           self.snake[self.head]['y'] == self.food['y']:
            return True
        else:
            return False


class GameState(PygameStarter):
    """Main program :
       Draw the grid, compute start and end animations
       Control the board boxes with the mouse/keyboard"""
    def __init__(self, title="WORM OR SNAKE ?", size=(640, 480), cell_size=20,
                 background=(60, 60, 60)):
        super().__init__(size=size, title=title, background=background)

        # Hide mouse
        pygame.mouse.set_visible(False)

        # Play music during the game (stop when game over, pause if game pause)
        self.son = pygame.mixer.Sound("Stock/match5.wav")
        pygame.mixer.music.load('Stock/ThinkTwice.mp3')
        pygame.mixer.music.play(-1, 0.0)

        # Start game welcome screen
        GameStart(size=SCREEN_SIZE).mainloop(FPS+5)

        # Cells parameters
        self.cell_size = cell_size
        self.cell_dimension = (int(self.size[0]/self.cell_size),
                               int(self.size[1]/self.cell_size))
        assert self.size[0] % self.cell_size == 0, "You must choice a cell size as a multiple of screen width"
        assert self.size[1] % self.cell_size == 0, "You must choice a cell size as a multiple of screen height"
        self.nb_cell = (self.size[0] / self.cell_size,
                        self.size[1] / self.cell_size)

        # Grid color
        self.grid_color = (70, 70, 70)

        # Prepare font (0 : score, 1 : game over)
        self.font = (pygame.font.Font('freesansbold.ttf', 18),
                     pygame.font.Font('freesansbold.ttf', 150))
        self.gameover_text = [None, None]  # Initialize the game over message

        # Add Snake
        self.snake = Snake(self.nb_cell, 3)
        self.snake_colors = ((0, 155, 0), (0, 255, 0))
        self.food_color = ((155, 0, 0), (255, 0, 0))

    def draw_grid(self):
        """Draw the background grid"""
        for x in range(0, self.size[0], self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.size[1]))
        for y in range(0, self.size[1], self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.size[0], y))

    def draw_food(self):
        """Draw food in random position"""
        x = self.snake.food['x'] * self.cell_size
        y = self.snake.food['y'] * self.cell_size
        food_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, self.food_color[0], food_rect)
        food_in = pygame.Rect(x+4, y+4, self.cell_size-8, self.cell_size-8)
        pygame.draw.rect(self.screen, self.food_color[1], food_in)

    def draw_snake(self):
        """Draw the snake"""
        for coords in self.snake.snake:
            x = coords['x'] * self.cell_size
            y = coords['y'] * self.cell_size
            snake_segment = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.snake_colors[0], snake_segment)
            snake_in = pygame.Rect(x+4, y+4, self.cell_size-8, self.cell_size-8)
            pygame.draw.rect(self.screen, self.snake_colors[1], snake_in)
            self.handle_quit()

    def prepare_text(self, text, font, color, x, y, pos="topleft"):
        """Prepare a text to be blit to the screen"""
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        if pos == "topleft":
            text_rect.topleft = x, y
        elif pos == "center":
            text_rect.center = x, y
        return (text_surf, text_rect)

    def draw_score(self):
        """Print in the screen the actual score"""
        self.screen.blit(self.score_text[0], self.score_text[1])

    def draw(self):
        self.screen.fill(self.background)
        self.draw_grid()
        self.draw_food()
        self.draw_snake()
        self.draw_score()

    def key_down(self, key):
        """Move the snake and avoid the half turns involving a collision"""
        if key in (K_LEFT, K_q) and self.snake.direction != RIGHT:
            self.snake.direction = LEFT
        elif key in (K_RIGHT, K_d) and self.snake.direction != LEFT:
            self.snake.direction = RIGHT
        elif key in (K_UP, K_z) and self.snake.direction != DOWN:
            self.snake.direction = UP
        elif key in (K_DOWN, K_s) and self.snake.direction != UP:
            self.snake.direction = DOWN
        elif key == K_p:
            self.pause()

    def check_states(self):
        """Check snake and apple state"""
        out = self.snake.game_over()
        eat = self.snake.has_eat()
        if out:
            # Game over
            self.new_game()
        elif eat:
            # Keep last snake segment
            self.snake.add_food()
            return
        else:
            # Remove last snake segment
            del self.snake.snake[-1]

    def update(self):
        """Check all states"""
        # Move snake
        self.snake.move_snake()
        self.check_states()
        # Change score text and prepare square base surface in top right corner
        self.score = len(self.snake.snake) - self.snake.length
        self.score_text = self.prepare_text('Score :  ' + str(self.score),
                                            self.font[0], (200, 200, 200),
                                            self.size[0]-120, 10)

    def new_game(self):
        """Create a new instance of a snake"""
        self.son.play()
        self.gameover_text[0] = self.prepare_text('Game', self.font[1],
                                                  (200, 200, 200),
                                                  self.size[0]/2,
                                                  self.size[1]*2/6, "center")
        self.gameover_text[1] = self.prepare_text('Over', self.font[1],
                                                  (200, 200, 200),
                                                  self.size[0]/2,
                                                  self.size[1]*4/6, "center")
        # Draw Game Over message on the screen
        self.screen.blit(self.gameover_text[0][0], self.gameover_text[0][1])
        self.screen.blit(self.gameover_text[1][0], self.gameover_text[1][1])
        pygame.display.update()
        pygame.time.wait(2000)  # Wait 2 sec to let player see his score

        # Restart to start screen and reinit the snake
        GameStart(size=SCREEN_SIZE).mainloop(FPS+5)
        self.snake = Snake(self.nb_cell, 3)

    def pause(self):
        """Pause the game"""
        pygame.mixer.music.pause()
        self.wait_for_key(K_p)
        pygame.mixer.music.unpause()
        pygame.time.wait(200)  # Avoid too fast move when resume game


class GameStart(PygameStarter):
    """Welcome game screen"""
    def __init__(self, title="WORM OR SNAKE ?", size=(640, 480),
                 background=(0, 100, 100)):
        super().__init__(size=size, title=title, background=background, init=False)

        # Colors
        self.colors = ((255, 255, 255), (0, 155, 0), (0, 255, 0))

        # Prepare font (memo : split and slicing used)
        self.font = (pygame.font.Font('freesansbold.ttf', 80),
                     pygame.font.Font('freesansbold.ttf', 18))
        self.title_surf = (self.font[0].render('Snake or Worm ?',
                                               True, *self.colors[:-1]),
                           self.font[0].render('Snake or Worm ?',
                                               True, self.colors[2]))
        self.instructions = self.font[1].render("Press enter key to play",
                                                True, (40, 40, 40))
        self.commands = self.font[1].render("Press < p > pause the game",
                                            True, (40, 40, 40))
        # Rotation states
        self.rotate = [0, 0]

    def draw_title(self):
        """Draw title on the screen"""
        rotated_surface1 = pygame.transform.rotate(self.title_surf[0],
                                                   self.rotate[0])
        rotated_surface2 = pygame.transform.rotate(self.title_surf[1],
                                                   self.rotate[1])

        rotated_rect1 = rotated_surface1.get_rect()
        rotated_rect1.center = (self.size[0]/2, self.size[1]/2)

        rotated_rect2 = rotated_surface2.get_rect()
        rotated_rect2.center = (self.size[0]/2, self.size[1]/2)

        self.screen.blit(rotated_surface1, rotated_rect1)
        self.screen.blit(rotated_surface2, rotated_rect2)

    def update(self):
        """Change rotation value each frames"""
        self.rotate[0] += 3
        self.rotate[1] += 7

    def draw_instruction(self):
        """Print how to play game"""
        instructions_rect = self.instructions.get_rect()
        instructions_rect.topleft = (self.size[0]-270, self.size[1]-60)
        self.screen.blit(self.instructions, instructions_rect)

    def draw_commands(self):
        """Print how to pause the game"""
        commands_rect = self.commands.get_rect()
        commands_rect.topleft = (self.size[0]-270, self.size[1]-30)
        self.screen.blit(self.commands, commands_rect)

    def draw(self):
        self.screen.fill(self.background)
        self.draw_title()
        self.draw_instruction()
        self.draw_commands()

    def key_up(self, key):
        """Check if a key is pressed"""
        if key == K_RETURN:
            # We stop the infinite loop but we don't call self.action_quit()
            # Allow to continue with the next game screen
            self.running = False


########################
#### Main Program : ####
########################


if __name__ == '__main__':
    main = GameState(size=SCREEN_SIZE, cell_size=40)
    main.mainloop(FPS)
