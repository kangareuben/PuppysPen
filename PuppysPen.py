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
import Constants
from Level import Level

class PuppysPen:

    # Runs before the game loop begins
    def __init__(self, _py_screen):
        self.running = True # controls the exit of the game loop
        self.clock = pygame.time.Clock() # controls the frame rate
        self.forceAll = False # force an entire repaint of the screen on the next frame
        self.clicked = None # the ID of the object that was clicked
        self.py_screen = _py_screen

        self.grid_offset = self.center_coords(600, 400)
        self.grid_width = 600
        self.grid_height = 400
        self.num_rows = 6
        self.num_columns = 6
        self.row_height = self.grid_height / self.num_rows
        self.column_width = self.grid_width / self.num_columns
        #print(self.row_height, self.column_width)

        self.font = pygame.font.Font(None, 36)

        self.level = Level(0, True)
        self.perimeter = self.level.level

        self.update()

        self.mouse_grid_position = (0, 0)
        self.mouse_prev_grid_position = (0, 0)
        self.rect_origin = (0, 0)
        self.drawing_rect = False

        #self.instruction_text_surface = self.font.render("Click once to start a rectangle, and again to finish it", True, (0, 0, 0))
        #self.instruction_text_pos = self.instruction_text_surface.get_rect()
        #self.instruction_text_pos.centerx = self.py_screen.get_rect().centerx

        #self.level_text_surface = self.font.render("Make a rectangle with perimeter " + str(self.perimeter), True, (0, 0, 0))
        #self.level_text_pos = self.level_text_surface.get_rect()
        #self.level_text_pos.centerx = self.py_screen.get_rect().centerx
        #self.level_text_pos.centery = self.py_screen.get_rect().centery - 300

    def update(self):
        self.draw_background()

        self.instruction_text_surface, self.instruction_text_pos = self.draw_text("Click once to start a rectangle, and again to finish it")
        self.instruction_text_pos.centerx = self.py_screen.get_rect().centerx

        self.level_text_surface, self.level_text_pos = self.draw_text("Make a rectangle with perimeter " + str(self.perimeter))
        self.level_text_pos.centerx = self.py_screen.get_rect().centerx
        self.level_text_pos.centery = self.py_screen.get_rect().centery - 300

        self.py_screen.blit(self.level_text_surface, self.level_text_pos)
        self.py_screen.blit(self.instruction_text_surface, self.instruction_text_pos)

        self.draw_grid(self.grid_offset[0], self.grid_offset[1], self.grid_width, self.grid_height, self.num_rows, self.num_columns)

    def draw_background(self, color=(84,171,71)):
        # grass green
        self.py_screen.fill(color)

    def draw_text(self, text, color=(0,0,0)):
        surface = self.font.render(text, True, color)
        pos = surface.get_rect()
        return surface, pos

    def center_coords(self, _w, _h):
        x_padding = int((Constants.WIDTH - _w) / 2.0)
        y_padding = int((Constants.HEIGHT - _h) / 2.0)
        print("center_coords", x_padding, y_padding)
        return (x_padding, y_padding)

    def draw_rectangle(self, _x, _y, _width, _height):
        pygame.draw.rect(self.py_screen, (255,255,255), (_x,_y,_width,_height), 1)

    def draw_grid(self, _x, _y, _width, _height, _num_rows, _num_columns):
        _row_height = int(_height / _num_rows)
        _column_width = int(_width / _num_columns)

        for i in range(0, _num_columns + 1):
            self.draw_rectangle(i * _column_width + _x, _y, 1, _height)

        for j in range(0, _num_rows + 1):
            self.draw_rectangle(_x, j * _row_height + _y, _width, 1)

    def begin_user_rectangle(self):
        self.drawing_rect = True
        self.rect_origin = self.mouse_grid_position

    def finish_user_rectangle(self):
        self.drawing_rect = False

        origin_x = int(self.grid_offset[0] + (self.rect_origin[0] * self.column_width))
        origin_y = int(self.grid_offset[1] + (self.rect_origin[1] * self.row_height))

        x_pos = int(self.grid_offset[0] + (self.mouse_grid_position[0] * self.column_width))
        y_pos = int(self.grid_offset[1] + (self.mouse_grid_position[1] * self.row_height))

        width = x_pos - origin_x
        height = y_pos - origin_y

        pygame.draw.rect(self.py_screen, (255, 0, 0), (origin_x, origin_y, width, height), 3)

        # Calculate perimeter of rectangle and check against level's perimeter
        rect_width = abs(self.mouse_grid_position[0] - self.rect_origin[0])
        rect_height = abs(self.mouse_grid_position[1] - self.rect_origin[1])
        
        rect_perimeter = 2 * rect_width + 2 * rect_height
        if rect_perimeter == self.perimeter:
            # Success! New level
            self.level = Level(0, True)
            self.perimeter = self.level.level
            
        else:
            # Wat? Retry level
            pass

    def get_offset_mouse(self):
        """ Returns a tuple (x,y) offset based on self.grid_offset """
        pos = pygame.mouse.get_pos()
        return (pos[0] - self.grid_offset[0], pos[1] - self.grid_offset[1])

    def get_grid_mouse(self, pos):
        mouse_x, mouse_y = pos

        if mouse_x <= 0 and mouse_y <= 0:
            mouse_grid_position = (0, 0)

        elif mouse_x > 0 and mouse_y > 0:
            grid_x = round(mouse_x / float(self.column_width))
            grid_y = round(mouse_y / float(self.row_height))
            mouse_grid_position = (grid_x, grid_y)
            print(mouse_x / float(self.column_width), mouse_y / float(self.row_height))
            #print(mouse_grid_position)

            if grid_x > self.num_columns:
                if grid_y > self.num_rows:
                    mouse_grid_position = (self.num_columns, self.num_rows)
                else:
                    mouse_grid_position = (self.num_columns, mouse_grid_position[1])

            if grid_y > self.num_rows:
                mouse_grid_position = (mouse_grid_position[0], self.num_rows)

        elif mouse_x <= 0:
            grid_y = round(mouse_y / self.row_height)

            if grid_y > self.num_rows:
                grid_y = self.num_rows

            mouse_grid_position = (0, grid_y)

        elif mouse_y <= 0:
            grid_x = round(mouse_x / self.column_width)

            if grid_x > self.num_columns:
                grid_x = self.num_columns

            mouse_grid_position = (grid_x, 0)

        return mouse_grid_position

    # Main game loop
    def run(self):
        self.main_screen = MainScreen(self.py_screen)
        self.play_screen = GameScreen(self.py_screen)

        # set the initial screen
        self.screen = self.main_screen

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
                    # Update mouse origin to grid position
                    mouse_x, mouse_y = self.get_offset_mouse()

                    # Update mouse_grid_position based on current mouse position
                    mouse_grid_x, mouse_grid_y = self.get_grid_mouse((mouse_x, mouse_y))
                    self.mouse_grid_position = (mouse_grid_x, mouse_grid_y)

                    # TODO: Empty mousemove handler at the moment
                    #self.screen.mousemove(pos)

                    # If mouse_grid position and mouse_prev_grid_position are different
                    if (mouse_grid_x, mouse_grid_y) != self.mouse_prev_grid_position:
                        self.update()
                        
                        x_pos = int(self.grid_offset[0] + (mouse_grid_x * self.column_width))
                        y_pos = int(self.grid_offset[1] + (mouse_grid_y * self.row_height))
                        
                        if not self.drawing_rect:
                            pygame.draw.circle(self.py_screen, (255, 255, 0), (x_pos, y_pos), 10)
                        
                        else:
                            origin_x = int(self.grid_offset[0] + (self.rect_origin[0] * self.column_width))
                            origin_y = int(self.grid_offset[1] + (self.rect_origin[1] * self.row_height))
                            
                            width = x_pos - origin_x
                            height = y_pos - origin_y

                            pygame.draw.rect(self.py_screen, (255, 0, 0), (origin_x, origin_y, width, height), 3)

                        self.mouse_prev_grid_position = self.mouse_grid_position

                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1 or event.button == 3:
                        #pos = pygame.mouse.get_pos()
                        #self.clicked = self.screen.click(pos)

                        # TODO: throw this in click event handler, only for the
                        # GameScreen
                        if not self.drawing_rect:
                            # Start drawing rectangle
                            self.begin_user_rectangle()

                        else:
                            # Finish drawing rectangle
                            self.finish_user_rectangle()

                elif event.type == QUIT:
                    self.running = False

class Screen(object):
    def __init__(self):
        pass

    def click(self, pos):
        """ Default click event handler """
        #print(pos)
        pass

    def mousemove(self, pos):
        """ Default mousemove event handler """
        #print(pos)
        pass

class MainScreen(Screen):
    def __init__(self, _py_screen):
        super(MainScreen, self).__init__()
        self.py_screen = _py_screen

class GameScreen(Screen):
    def __init__(self, _py_screen):
        super(GameScreen, self).__init__()

# This function is called when the game is run directly from the command line:
# ./PuppysPen.py
def main():
    pygame.init()
    py_screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), \
            pygame.RESIZABLE) # 54 = height of sugar toolbar
    game = PuppysPen(py_screen)
    game.run()

if __name__ == '__main__':
    main()
