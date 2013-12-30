#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""HELPER FOR MAIN CLASS OF A PYTHON PROGRAM"""

###########################################
#### Importation fonction et modules : ####
###########################################

import sys
import pygame
from pygame.locals import *


##############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : ####
##############################################################################


class PygameStarter:
    """A class which defines a starter to create a pygame application
        Initiate the main window with size and background color
        Handle_events : keyboard and mouse
        Print the current application FPS
        Start the mainloop by calling self.mainloop()
                                                     """
    def __init__(self, size=(640, 480), background=(255, 255, 255), title="Game"):
        pygame.init()
        self.screen = pygame.display.set_mode(size, 0, 32)
        self.screen.fill(background)
        pygame.display.flip()  # Update the entire content
        self.running = False  # Wait for mainloop to start
        self.clock = pygame.time.Clock()  # Track FPS
        self.size = size  # Size of the screen
        self.fps = 0  # Define FPS when start mainloop
        self.time_passed = 0  # Compute time passed since last loop
        self.background = background
        self.title = title
        pygame.display.set_caption(self.title)

    # Handle events
    def handle_events(self):
        """Detect events from mouse and keyboard. Also handle quit event"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False  # Quit
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.running = False  # Quit (useful when mouse hide/block)
                else:
                    self.key_up(event.key)
            elif event.type == KEYDOWN:
                self.key_down(event.key)
            elif event.type == MOUSEBUTTONUP:
                self.mouse_up(event.button, event.pos)
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_down(event.button, event.pos)
            elif event.type == MOUSEMOTION:
                self.mouse_motion(event.buttons, event.pos, event.rel)

    # Wait for key (pressed)
    def wait_for_key(self):
        """Wait for key pressed"""
        press = False
        while not press:
            for event in pygame.event.get():
                if event.type == KEYUP:
                    press = True

    # Enter the main loop
    def mainloop(self, fps=0):
        """Start the program mainloop"""
        self.running = True
        self.fps = fps
        while self.running:
            self.start_actions()
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.time_passed = self.clock.tick(self.fps)
            self.restart()
        # Close pygame properly if user try to quit
        self.action_quit()

    def handle_quit(self):
        """Recup all quit event to force quit inside other methode, function, ...
           Should be use inside long loop"""
        for event in pygame.event.get(QUIT):  # get all the QUIT events
            self.running = False
            self.action_quit()
        for event in pygame.event.get(KEYUP):  # get all the KEYUP events
            if event.key == K_ESCAPE:
                self.running = False
                self.action_quit()
            pygame.event.post(event)  # add other KEYUP event to queue

    def action_quit(self):
        """Print quit message and quit pygame window properly"""
        print(' Pygame says Good Bye ')
        pygame.quit()
        sys.exit()

    def update(self):
        pass

    def draw(self):
        pass

    def key_down(self, key):
        pass

    def key_up(self, key):
        pass

    def mouse_up(self, button, pos):
        pass

    def mouse_down(self, button, pos):
        pass

    def mouse_motion(self, buttons, pos, rel):
        pass

    def restart(self):
        pass

    def start_actions(self):
        pass

###############################
#### Programme principal : ####
###############################


if __name__ == '__main__':

    from vector2d import *

    class PygameMain(PygameStarter):
        """Main program handle_events and mainloop"""
        def __init__(self):
            self.size = (300, 300)
            super().__init__(self.size)  # Inherit from PygameStarter
            self.cat = pygame.image.load("cat.png")
            self.cat_pos = Vector2D(10, 10)
            self.cat_speed = 100
            self.cat_direction = Vector2D(1, 0)

        def update(self):
            self.mouvement()
            time_passed_seconds = self.time_passed / 1000.0
            self.cat_pos += time_passed_seconds * self.cat_direction * self.cat_speed

        def draw(self):
            self.screen.fill(self.background)
            self.screen.blit(self.cat, self.cat_pos)

        def mouvement(self):
            # Keep the cat around the screen
            if self.cat_pos[0] > self.size[0] - self.cat.get_width():
                # To avoid conflicts
                self.cat_pos[0] = self.size[0] - self.cat.get_width()
                self.cat_direction = Vector2D(0, 1)

            elif self.cat_pos[0] < 0:
                # To avoid conflicts
                self.cat_pos[0] = 0
                self.cat_direction = Vector2D(0, -1)

            elif self.cat_pos[1] > self.size[1] - self.cat.get_height():
                # To avoid conflicts
                self.cat_pos[1] = self.size[1] - self.cat.get_height()
                self.cat_direction = Vector2D(-1, 0)

            elif self.cat_pos[1] < 0:
                # To avoid conflicts
                self.cat_pos[1] = 0
                self.cat_direction = Vector2D(1, 0)

    mainClass = PygameMain()  # Create mainProgram
    mainClass.mainloop(60)  # Start mainProgram
