#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""HELPER FOR MAIN CLASS OF A PYTHON PROGRAM"""

########################################
#### Classes and Methods imported : ####
########################################

import sys
import pygame
from pygame.locals import *


#######################################
#### Classes, Methods, Functions : ####
#######################################


class PygameStarter:
    """

        A class which defines a starter to create a pygame application.

        Initiate the main window with size and background color
        Handle_events : keyboard and mouse
        Start the mainloop by calling self.mainloop()

     """

    def __init__(self, size=(640, 480), background=(255, 255, 255),
                 title="Game", init=True):

        # Allow to init only if needed
        self.init = init
        if self.init:
            pygame.init()

        # Minimal window elements
        self.screen = pygame.display.set_mode(size, 0, 32)
        self.screen.fill(background)
        self.title = title
        pygame.display.set_caption(self.title)
        pygame.display.flip()  # Update the entire content

        self.running = False  # Allow to create a game instance without running it
        self.clock = pygame.time.Clock()  # Track FPS
        self.size = size  # Size of the screen
        self.fps = 0  # Keep trace of game FPS
        self.time_passed = 0  # Compute time passed since last loop
        self.background = background

    # Handle events
    def handle_events(self):
        """Detect events from mouse and keyboard. Also handle quit event"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False  # Quit
                self.action_quit()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.running = False  # Quit (useful when mouse hide/block)
                    self.action_quit()
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

    def handle_quit(self):
        """Recup all quit event to force quit inside other methode, function, ...
           Should be use inside long loop to break it and quit a program"""
        for event in pygame.event.get(QUIT):  # get all the QUIT events
            self.running = False
            self.action_quit()
        for event in pygame.event.get(KEYUP):  # get all the KEYUP events
            if event.key == K_ESCAPE:
                self.running = False
                self.action_quit()
            pygame.event.post(event)  # add other KEYUP event to queue

    # Wait until a specific key is pressed
    def wait_for_key(self, key):
        """Wait for key pressed"""
        press = False
        # Pause game and clear events list
        # Avoid leaving pause mode without meaning to
        pygame.time.wait(100)
        pygame.event.clear()  # Clear events
        while not press:
            for event in pygame.event.get():
                if event.type == KEYUP and event.key == key:
                    press = True
            # Limit loop speed with clock.tick which spends less CPU usage
            # than pygame.time.wait
            self.clock.tick(self.fps)
            self.handle_quit()  # Check for QUIT events

    # Enter the main loop
    def mainloop(self, fps=0):
        """Start the program mainloop which calls methods every loops"""
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
        return

    def action_quit(self):
        """Print quit message and quit pygame window properly"""
        print(' Pygame says Good Bye ')
        pygame.quit()
        sys.exit()

    def prepare_text(self, text, font, color, x, y, bg_color=None,
                     pos="topleft"):
        """
            Prepare a text to be blit to the screen.

            Necessary :
            text : Text to print on the window
            font : Pygame.font.Font
            color : Text color
            x, y : Pixel coordinates to define where to draw

            Optional
            bg_color : Background color
            pos : Define if x and y are topleft or center coordinates

        """
        if bg_color:
            text_surf = font.render(text, True, color, bg_color)
        else:
            text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        if pos == "topleft":
            text_rect.topleft = x, y
        elif pos == "center":
            text_rect.center = x, y
        return (text_surf, text_rect)

    def update(self):
        pass

    def draw(self):
        """Draw all shapes and pictures on the screen surface"""
        pass

    def key_down(self, key):
        """Called when a key is pushed"""
        pass

    def key_up(self, key):
        """Called when a key is released"""
        pass

    def mouse_up(self, button, pos):
        """Called when mouse clic is released"""
        pass

    def mouse_down(self, button, pos):
        """Called when mouse clic is pushed"""
        pass

    def mouse_motion(self, buttons, pos, rel):
        """Call when mouse is moved"""
        pass

    def restart(self):
        """Compute some update to some variables before run an other loop"""
        pass

    def start_actions(self):
        """Compute some update when new loop begins"""
        pass

########################
#### Main Program : ####
########################


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
