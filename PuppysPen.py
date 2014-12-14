"""
The MIT License (MIT)

Copyright (c) 2014 kangareuben

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#!/usr/bin/python
'''
Primary pygame file. Deals with all the stuff.

Application structure taken from brendanwhitfield/planetary
'''

# python
import random
import os

# gtk
from gi.repository import Gtk

# pygame
import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, VIDEORESIZE, ACTIVEEVENT

# app
from Constants import HEIGHT, WIDTH, GREEN, DARKGREY, GREY, LIGHTGREY, MAROON
from Screens import GameScreen, MainScreen

class PuppysPen:
    # Runs before the game loop begins
    def __init__(self, _py_screen):
        # controls the exit of the game loop
        self.running = True
        # controls the frame rate
        self.clock = pygame.time.Clock()
        # force an entire repaint of the screen on the next frame
        self.forceAll = False
        self.py_screen = _py_screen
        self.font_reg = os.path.join("resources", "Arvo-Regular.ttf")
        self.font_bold = os.path.join("resources", "Arvo-Bold.ttf")
        self.font = pygame.font.Font(self.font_reg, 36)
        self.rect_origin = (0, 0)
        self.screen = None
        self.update()

    def update(self):
        self.draw_background()
        if self.screen: self.screen.update()

    def draw_background(self, color=GREEN):
        # grass green
        self.py_screen.fill(color)

    def draw_text(self, text, pyfont=None, color=DARKGREY):
        if not pyfont: pyfont = self.font
        surface = pyfont.render(text, True, color)
        pos = surface.get_rect()
        return surface, pos

    def center_coords(self, _w, _h):
        # TODO: make responsive not just xo size
        x_padding = int((WIDTH - _w) / 2.0)
        y_padding = int((HEIGHT - _h) / 2.0)
        print("center_coords", x_padding, y_padding)
        return (x_padding, y_padding)

    def draw_rectangle(self, _x, _y, _width, _height):
        pygame.draw.rect(self.py_screen, LIGHTGREY, (_x,_y,_width,_height), 1)

    def switch_screen(self, screen, new_game=False):
        print(self.main_screen.first_time)
        if screen.lower() == "main" or screen.lower() == "home":
            self.screen = self.main_screen

        elif screen.lower() == "game" or screen.lower() == "play":
            if new_game: self.game_screen = GameScreen(self.py_screen, self)
            self.screen = self.game_screen
            self.main_screen.first_time = False
        self.update()

    # Main game loop
    def run(self):
        self.main_screen = MainScreen(self.py_screen, self)
        self.game_screen = GameScreen(self.py_screen, self)

        # set the initial screen
        self.screen = self.main_screen
        self.update()

        # The main game loop.
        while self.running:
            # Should we be using the blit() method to draw things to the screen each frame?
            # If so, this seems like a good tutorial
            # https://www.pygame.org/docs/tut/tom/games2.html

            # Pump GTK events
            while Gtk.events_pending():
                Gtk.main_iteration()

            pygame.display.update()
            self.clock.tick(30)

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == MOUSEMOTION:
                    # Update mouse origin to grid position
                    self.screen.mouse_move(pos)

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:
                        self.screen.mouse_down(pos)

                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1 or event.button == 3:
                        self.screen.mouse_up(pos)

                elif event.type == QUIT:
                    self.running = False

# This function is called when the game is run directly from the command line:
# ./PuppysPen.py
def main():
    pygame.init()
    py_screen = pygame.display.set_mode((WIDTH, HEIGHT), \
            pygame.RESIZABLE) # 54 = height of sugar toolbar
    game = PuppysPen(py_screen)
    game.run()

if __name__ == '__main__':
    main()
