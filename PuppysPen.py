#!/usr/bin/python
'''
Primary pygame file. Deals with all the stuff.

Application structure taken from brendanwhitfield/planetary
'''

# python
import random

# gtk
from gi.repository import Gtk

# pygame
import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP, MOUSEMOTION, VIDEORESIZE, ACTIVEEVENT

# app
from Constants import HEIGHT, WIDTH, GREEN, DARKGREY, GREY, LIGHTGREY, MAROON
from Screens import GameScreen, MainScreen

class PuppysPen:

    # Runs before the game loop begins
    def __init__(self, _py_screen):
        self.running = True # controls the exit of the game loop
        self.clock = pygame.time.Clock() # controls the frame rate
        self.forceAll = False # force an entire repaint of the screen on the next frame
        self.clicked = None # the ID of the object that was clicked
        self.py_screen = _py_screen
        self.font = pygame.font.Font("resources/Arvo-Regular.ttf", 36)
        self.rect_origin = (0, 0)
        self.screen = None
        self.update()

    def update(self):
        self.draw_background()
        if self.screen: self.screen.update()

    def draw_background(self, color=GREEN):
        # grass green
        self.py_screen.fill(color)

    def draw_text(self, text, color=(0,0,0)):
        surface = self.font.render(text, True, color)
        pos = surface.get_rect()
        return surface, pos

    def center_coords(self, _w, _h):
        # TODO: make responsive not just xo size
        x_padding = int((WIDTH - _w) / 2.0)
        y_padding = int((HEIGHT - _h) / 2.0)
        print("center_coords", x_padding, y_padding)
        return (x_padding, y_padding)

    def draw_rectangle(self, _x, _y, _width, _height):
        pygame.draw.rect(self.py_screen, (255,255,255), (_x,_y,_width,_height), 1)

    def switch_screen(self, screen):
        if screen.lower() == "main" or screen.lower() == "home":
            self.screen = self.main_screen
        elif screen.lower() == "game" or screen.lower() == "play":
            self.screen = self.game_screen
        self.update()

    # Main game loop
    def run(self):
        self.main_screen = MainScreen(self.py_screen, self)
        self.game_screen = GameScreen(self.py_screen, self)

        # set the initial screen
        self.screen = self.main_screen
        #self.screen = self.game_screen
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
                if event.type == MOUSEMOTION:
                    #mouse_x, mouse_y = self.get_offset_mouse()
                    # Update mouse origin to grid position
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.screen.mousemove((mouse_x, mouse_y))

                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1 or event.button == 3:
                        pos = pygame.mouse.get_pos()
                        self.clicked = self.screen.click(pos)

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
