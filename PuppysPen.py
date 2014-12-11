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
from pygame.locals import QUIT, MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, VIDEORESIZE, ACTIVEEVENT

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

        self.grid_width = 600
        self.grid_height = 600
        self.grid_offset = self.center_coords(self.grid_width, self.grid_height)
        self.num_rows = 6
        self.num_columns = 6
        self.row_height = self.grid_height / self.num_rows
        self.column_width = self.grid_width / self.num_columns

        self.font = pygame.font.Font(None, 36)

        self.recent_levels = []
        self.max_recent_levels = 1
        self.matches_recent_level = False
        
        self.level = Level(0, False, True, (self.num_rows, self.num_columns))
        self.area = self.level.level
        self.perimeter = 0
        
        self.recent_levels.insert(0, self.area)
        
        self.feedback_string = ""
        self.level_count = 0

        self.update()

        self.mouse_grid_position = (0, 0)
        self.mouse_prev_grid_position = (0, 0)
        self.rect_origin = (0, 0)
        self.drawing_rect = False

    def update(self):
        self.draw_background()

        self.instruction_text_surface, self.instruction_text_pos = self.draw_text("Click and drag to create a rectangle")
        self.instruction_text_pos.centerx = self.py_screen.get_rect().centerx
        self.instruction_text_pos.centery = self.py_screen.get_rect().centery - 385
        
        if self.level_count % 15 < 5:
            self.level_text_surface, self.level_text_pos = self.draw_text("Make a rectangle with area " + str(self.area))
        
        elif self.level_count % 15 < 10:
            self.level_text_surface, self.level_text_pos = self.draw_text("Make a rectangle with perimeter " + str(self.perimeter))
            
        else:
            self.level_text_surface, self.level_text_pos = self.draw_text("Make a rectangle with area " + str(self.area) + " and perimeter " + str(self.perimeter))
        
        self.level_text_pos.centerx = self.py_screen.get_rect().centerx
        self.level_text_pos.centery = self.py_screen.get_rect().centery - 345
        
        self.level_count_text_surface, self.level_count_text_pos = self.draw_text("Level: " + str(self.level_count + 1))
        self.level_count_text_pos.centerx = self.py_screen.get_rect().centerx - 520
        self.level_count_text_pos.centery = self.py_screen.get_rect().centery - 385

        self.py_screen.blit(self.level_text_surface, self.level_text_pos)
        self.py_screen.blit(self.instruction_text_surface, self.instruction_text_pos)
        self.py_screen.blit(self.level_count_text_surface, self.level_count_text_pos)

        self.draw_grid()

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

    def draw_grid(self):
        self.row_height = float(self.grid_height) / float(self.num_rows)
        self.column_width = float(self.grid_width) / float(self.num_columns)

        # Draw the 0 only once
        self.font = pygame.font.Font(None, 20)
            
        self.grid_number_text_surface, self.grid_number_text_pos = self.draw_text(str(0))
        self.grid_number_text_pos.centerx = self.grid_offset[0] - 13
        self.grid_number_text_pos.centery = self.grid_offset[1] - 13
        self.py_screen.blit(self.grid_number_text_surface, self.grid_number_text_pos)
        
        self.font = pygame.font.Font(None, 36)

        for i in range(0, self.num_columns + 1):
            self.draw_rectangle(i * self.column_width + self.grid_offset[0], self.grid_offset[1], 1, self.grid_height)
            
            if i > 0:
                # Draw grid numbers
                self.font = pygame.font.Font(None, 20)
                
                self.grid_number_text_surface, self.grid_number_text_pos = self.draw_text(str(i))
                self.grid_number_text_pos.centerx = i * self.column_width + self.grid_offset[0]
                self.grid_number_text_pos.centery = self.grid_offset[1] - 14
                self.py_screen.blit(self.grid_number_text_surface, self.grid_number_text_pos)
                
                self.font = pygame.font.Font(None, 36)

        for j in range(0, self.num_rows + 1):
            self.draw_rectangle(self.grid_offset[0], j * self.row_height + self.grid_offset[1], self.grid_width, 1)
            
            if j > 0:
                self.font = pygame.font.Font(None, 20)
                
                self.grid_number_text_surface, self.grid_number_text_pos = self.draw_text(str(j))
                self.grid_number_text_pos.centerx = self.grid_offset[0] - 14
                self.grid_number_text_pos.centery = j * self.row_height + self.grid_offset[1]
                self.py_screen.blit(self.grid_number_text_surface, self.grid_number_text_pos)
                
                self.font = pygame.font.Font(None, 36)

    def begin_user_rectangle(self):
        """ Starts drawing a user rectangle """
        self.drawing_rect = True
        self.rect_origin = self.mouse_grid_position

    def finish_user_rectangle(self):
        """ Stops drawing a user rectangle and calculates whether the rectangle met criteria """
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
        
        # Prevent users from drawing a rectangle with width or height 0
        if rect_width == 0 and rect_height == 0:
            self.level_failure("Not quite! Try drawing a rectangle instead of a point!")
        
        elif rect_width == 0 or rect_height == 0:
            self.level_failure("Not quite! Try drawing a rectangle instead of a line!")
        
        else:
            # Levels 1-5 are area only
            if self.level_count % 15 < 5:
                rect_area = rect_width * rect_height
                
                if rect_area == self.area:
                    # Success! New level
                    self.level_success()
                
                else:
                    # Wat? Retry level
                    self.level_failure()
            
            # Levels 6-10 are perimeter only
            elif self.level_count % 15 < 10:
                rect_perimeter = 2 * rect_width + 2 * rect_height
                
                if rect_perimeter == self.perimeter:
                    # Success! New level
                    self.level_success()
                    
                else:
                    # Wat? Retry level
                    self.level_failure()
            
            # Levels 11-15 are area and perimeter
            else:
                rect_area = rect_width * rect_height
                rect_perimeter = 2 * rect_width + 2 * rect_height
                
                if rect_area == self.area and rect_perimeter == self.perimeter:
                    # Success! New level
                    self.level_success()
                
                else:
                    # Wat? Retry level
                    self.level_failure()
            
            
        self.feedback_text_surface, self.feedback_text_pos = self.draw_text(self.feedback_text)
        self.feedback_text_pos.centerx = self.py_screen.get_rect().centerx
        self.feedback_text_pos.centery = self.py_screen.get_rect().centery + 350
        self.py_screen.blit(self.feedback_text_surface, self.feedback_text_pos)
        
    def level_success(self):
        """ Gives positive feedback to the user and generates a new level """
        self.feedback_text = "Well done!"
        self.level_count += 1
        
        # Make the grid bigger every 15 levels
        if self.level_count % 15 == 0:
            self.num_rows += 2
            self.num_columns += 2
        
        if self.level_count % 15 < 5:
            # Loop until you find a level that isn't the same as the previous max_recent_levels
            while True:
                self.matches_recent_level = False
                
                # Generate new area level
                self.level = Level(0, False, True, (self.num_rows, self.num_columns))
                self.area = self.level.level
                
                # Make sure it doesn't match any recent levels
                for x in range(self.max_recent_levels):
                    if self.area == self.recent_levels[x]:
                        self.matches_recent_level = True
                    
                if not self.matches_recent_level:
                    self.recent_levels.insert(0, self.area)
                    break
        
        elif self.level_count % 15 < 10:
            while True:
                self.matches_recent_level = False
                
                self.level = Level(0, True, False, (self.num_rows, self.num_columns))
                self.perimeter = self.level.level
                
                for x in range(self.max_recent_levels):
                    if self.perimeter == self.recent_levels[x]:
                        self.matches_recent_level = True
                    
                if not self.matches_recent_level:
                    self.recent_levels.insert(0, self.perimeter)
                    break
            
        else:
            while True:
                self.matches_recent_level = False
                
                self.level = Level(0, True, True, (self.num_rows, self.num_columns))
                self.area = self.level.level[0]
                self.perimeter = int(self.level.level[1])
                
                for x in range(self.max_recent_levels):
                    if self.area == self.recent_levels[x]:
                        self.matches_recent_level = True
                    
                if not self.matches_recent_level:
                    self.recent_levels.insert(0, self.area)
                    break
    
    def level_failure(self, _feedback_text="Oops, try again :("):
        """ Gives feedback to the user about what went wrong on this attempt """
        self.feedback_text = _feedback_text

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
                            pygame.draw.circle(self.py_screen, (255, 255, 0), (x_pos, y_pos), 7)
                        
                        else:
                            origin_x = int(self.grid_offset[0] + (self.rect_origin[0] * self.column_width))
                            origin_y = int(self.grid_offset[1] + (self.rect_origin[1] * self.row_height))
                            
                            width = x_pos - origin_x
                            height = y_pos - origin_y

                            pygame.draw.rect(self.py_screen, (255, 0, 0), (origin_x, origin_y, width, height), 3)

                        self.mouse_prev_grid_position = self.mouse_grid_position

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:
                        if not self.drawing_rect:
                            self.begin_user_rectangle()

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
                            if not self.mouse_grid_position == self.rect_origin:
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
