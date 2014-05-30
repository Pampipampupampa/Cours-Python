#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""Starting with pyglet"""

########################################
#### Classes and Methods imported : ####
########################################

import pyglet
from pyglet.window import key
from pyglet.window import mouse

# Check for AVbin
try:
    from pyglet.media import avbin
except ImportError:
    print('AVbin is required for this example, see ',
          'http://code.google.com/p/avbin')

#######################################
#### Classes, Methods, Functions : ####
#######################################


class MainWindow(pyglet.window.Window):
    """
        Create a new pyglet windows by inherite from pyglet window constructor.
            - on_draw is overloading to add some stuff on the screen.
    """
    def __init__(self, width, height):
        super().__init__(width=width, height=height)

        # Add an event logger which print windows events
        # self.push_handlers(pyglet.window.event.WindowEventLogger())

        # Add some text
        self.label = pyglet.text.Label('Hello, world',
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=self.width//2, y=self.height//2,
                                       anchor_x='center', anchor_y='center')

        # Add pictures
        # pyglet.image.load used if image not bundled with application
        # pyglet.resource.image used if image is a relative path from .py file
        self.image = pyglet.resource.image('kitten.jpg')

        # Add sounds and music
        # pyglet.media.load
        # pyglet.resource.media
        try:
            self.music = pyglet.resource.media('guitar.ogg')
            self.music.play()
        except pyglet.media.riff.WAVEFormatException as e:
            print(e)
        self.sound = pyglet.resource.media('ball.wav', streaming=False)
        self.sound.play()

    def on_draw(self):
        """Decorator used to tell him : it's an event handler"""
        self.clear()  # Clean window
        self.label.draw()  # Add text on the screen
        self.image.blit(0, self.height-self.image.height)

    def on_key_press(self, symbol, modifiers):
        """
            Keyboard events have two parameters:
                - the virtual key symbol that was pressed
                - a bitwise combination of any modifiers that are present
                  (for example, the CTRL and SHIFT keys).
        """
        if symbol == key.A and (modifiers & (key.MOD_CTRL | key.MOD_ALT)):
            print('The "A" key was pressed with CTRL or ALT.')
        elif symbol == key.LEFT and (modifiers & key.MOD_CTRL):
            print('The left arrow key was pressed with CTRL key holded.')
        elif symbol == key.ENTER:
            print('The enter key was pressed.')
        elif symbol == key.ESCAPE:
            self.on_close()

    def on_mouse_press(self, x, y, button, modifiers):
        """
            The x and y parameters give the position of the mouse
            when the button was pressed, relative to the lower-left corner
            of the window
        """
        if button == mouse.LEFT:
            print('The left mouse button was pressed at {}::{}'.format(x, y))
        elif button == mouse.RIGHT and (modifiers & key.MOD_CTRL):
            print('The right mouse button was pressed with CTRL key')


########################
#### Main Program : ####
########################

window = MainWindow(800, 600)


if __name__ == '__main__':
    pyglet.app.run()
