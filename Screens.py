"""
Where the two game states logic lives
"""
# python
import random

# pygame
import pygame

from Level import Level
from Constants import HEIGHT, WIDTH, GREEN, DARKGREY, GREY, LIGHTGREY, MAROON

class Screen(object):
    def __init__(self):
        """ A screen object should implement the following methods """
        pass

    def mouse_up(self, pos):
        """ Default mouse_up event handler """
        pass

    def mouse_down(self, pos):
        """ Default mouse_down event handler """
        pass

    def mouse_move(self, pos):
        """ Default mouse_move event handler """
        pass

    def update(self):
        """ Called in the main game loop """
        pass

class MainScreen(Screen):
    def __init__(self, _py_screen, _game):
        super(MainScreen, self).__init__()
        self.py_screen = _py_screen
        self.game = _game
        self.button_list = []

    def update(self):
        self.button_list.append(Button(self.game, (10, 10), 90, 25, "Start Game", self.game_event))

    def game_event(self):
        print("Go Back to game screen")
        self.game.switch_screen("game")

    def mouse_up(self, pos):
        for btn in self.button_list:
            if btn.is_mouse_over(pos):
                btn.call()
                return True

class GameScreen(Screen):
    def __init__(self, _py_screen, _game):
        super(GameScreen, self).__init__()
        self.game = _game
        self.py_screen = _py_screen

        self.rect_origin = (0, 0)
        self.mouse_grid_position = (0, 0)
        self.mouse_prev_grid_position = (0, 0)
        self.drawing_rect = False

        self.button_list = []

        self.grid_width = 600
        self.grid_height = 600
        self.grid_offset = self.game.center_coords(self.grid_width, self.grid_height)
        self.num_rows = 6
        self.num_columns = 6
        self.row_height = self.grid_height / self.num_rows
        self.column_width = self.grid_width / self.num_columns

        self.recent_levels = []
        self.level = Level(0, False, True, (self.num_rows, self.num_columns))
        self.area = self.level.level
        self.perimeter = 0
        self.level_count = 0
        self.recent_levels.insert(self.level_count, self.area)

        self.max_recent_levels = 1
        self.matches_recent_level = False
        self.feedback_string = ""

    def draw_grid(self):
        self.row_height = float(self.grid_height) / float(self.num_rows)
        self.column_width = float(self.grid_width) / float(self.num_columns)

        # Draw the 0 only once
        num_font = pygame.font.Font(self.game.font_reg, 20)

        self.grid_number_text_surface, self.grid_number_text_pos = self.game.draw_text(str(0), num_font)
        self.grid_number_text_pos.centerx = self.grid_offset[0] - 13
        self.grid_number_text_pos.centery = self.grid_offset[1] - 13
        self.py_screen.blit(self.grid_number_text_surface, self.grid_number_text_pos)

        for i in range(0, self.num_columns + 1):
            self.game.draw_rectangle(i * self.column_width + self.grid_offset[0], self.grid_offset[1], 1, self.grid_height)

            if i > 0:
                # Draw grid numbers
                self.grid_number_text_surface, self.grid_number_text_pos = self.game.draw_text(str(i), num_font)
                self.grid_number_text_pos.centerx = i * self.column_width + self.grid_offset[0]
                self.grid_number_text_pos.centery = self.grid_offset[1] - 14
                self.py_screen.blit(self.grid_number_text_surface, self.grid_number_text_pos)

        for j in range(0, self.num_rows + 1):
            self.game.draw_rectangle(self.grid_offset[0], j * self.row_height + self.grid_offset[1], self.grid_width, 1)

            if j > 0:
                self.grid_number_text_surface, self.grid_number_text_pos = self.game.draw_text(str(j), num_font)
                self.grid_number_text_pos.centerx = self.grid_offset[0] - 14
                self.grid_number_text_pos.centery = j * self.row_height + self.grid_offset[1]
                self.py_screen.blit(self.grid_number_text_surface, self.grid_number_text_pos)

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

        pygame.draw.rect(self.py_screen, MAROON, (origin_x, origin_y, width, height), 3)

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

        self.feedback_text_surface, self.feedback_text_pos = self.game.draw_text(self.feedback_text)
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

    def level_success(self):
        """ Gives positive feedback to the user and generates a new level """
        self.feedback_text = "Well done!"
        self.level_count += 1

        # Make the grid bigger every 15 levels
        if self.level_count % 15 == 0:
            self.num_rows += 2
            self.num_columns += 2
            self.row_height = self.grid_height / self.num_rows
            self.column_width = self.grid_width / self.num_columns

        if self.level_count % 15 < 5:
            self.level = Level(0, False, True, (self.num_rows, self.num_columns))
            self.area = self.level.level

        elif self.level_count % 15 < 10:
            self.level = Level(0, True, False, (self.num_rows, self.num_columns))
            self.perimeter = self.level.level

        else:
            self.level = Level(0, True, True, (self.num_rows, self.num_columns))
            self.area = self.level.level[0]
            self.perimeter = int(self.level.level[1])

    def level_failure(self, _feedback_text="Oops, try again :("):
        """ Gives feedback to the user about what went wrong on this attempt """
        self.feedback_text = _feedback_text

    def get_offset_mouse(self, pos):
        """ Returns a tuple (x,y) offset based on self.grid_offset """
        return (pos[0] - self.grid_offset[0], pos[1] - self.grid_offset[1])

    # pre-merge
    #def get_offset_mouse(self):
        #""" Returns a tuple (x,y) offset based on self.grid_offset """
        #pos = pygame.mouse.get_pos()
        #return (pos[0] - self.grid_offset[0], pos[1] - self.grid_offset[1])

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

    # pre-merge
    #def get_grid_mouse(self, pos):
        #mouse_x, mouse_y = pos

        #if mouse_x <= 0 and mouse_y <= 0:
            #mouse_grid_position = (0, 0)

        #elif mouse_x > 0 and mouse_y > 0:
            #grid_x = round(mouse_x / float(self.column_width))
            #grid_y = round(mouse_y / float(self.row_height))
            #mouse_grid_position = (grid_x, grid_y)

            #if grid_x > self.num_columns:
                #if grid_y > self.num_rows:
                    #mouse_grid_position = (self.num_columns, self.num_rows)
                #else:
                    #mouse_grid_position = (self.num_columns, mouse_grid_position[1])

            #if grid_y > self.num_rows:
                #mouse_grid_position = (mouse_grid_position[0], self.num_rows)

        #elif mouse_x <= 0:
            #grid_y = round(mouse_y / self.row_height)

            #if grid_y > self.num_rows:
                #grid_y = self.num_rows

            #mouse_grid_position = (0, grid_y)

        #elif mouse_y <= 0:
            #grid_x = round(mouse_x / self.column_width)

            #if grid_x > self.num_columns:
                #grid_x = self.num_columns

            #mouse_grid_position = (grid_x, 0)

        #return mouse_grid_position

    def update(self):
        self.instruction_text_surface, self.instruction_text_pos = \
            self.game.draw_text("Click and drag to create a rectangle")
        self.instruction_text_pos.centerx = self.py_screen.get_rect().centerx
        self.instruction_text_pos.centery = self.py_screen.get_rect().centery - 385

        if self.level_count % 15 < 5:
            level_text = "Make a rectangle with area " + str(self.area)

        elif self.level_count % 15 < 10:
            level_text = "Make a rectangle with perimeter " + str(self.perimeter)
        else:
            level_text = "Make a rectangle with area " + str(self.area) + \
                         " and perimeter " + str(self.perimeter) 

        self.level_text_surface, self.level_text_pos = \
            self.game.draw_text(level_text)

        self.level_text_pos.centerx = self.py_screen.get_rect().centerx
        self.level_text_pos.centery = self.py_screen.get_rect().centery - 345

        self.level_count_text_surface, self.level_count_text_pos = \
            self.game.draw_text("Level: " + str(self.level_count + 1))
        self.level_count_text_pos.centerx = self.py_screen.get_rect().centerx + 520
        self.level_count_text_pos.centery = self.py_screen.get_rect().centery - 385

        self.py_screen.blit(self.level_text_surface, self.level_text_pos)
        self.py_screen.blit(self.instruction_text_surface, self.instruction_text_pos)
        self.py_screen.blit(self.level_count_text_surface, self.level_count_text_pos)

        self.draw_grid()

        self.button_list.append(Button(self.game, (10, 10), 90, 25, "Go Back", self.back_event))

    def back_event(self):
        print("Go Back to main screen")
        self.game.switch_screen("main")

    def mouse_up(self, pos):
        for btn in self.button_list:
            if btn.is_mouse_over(pos):
                btn.call()
                return True

        if not self.drawing_rect:
            # Start drawing rectangle
            self.begin_user_rectangle()
        else:
            # Finish drawing rectangle
            self.finish_user_rectangle()

    def mouse_down(self, pos):
        if not self.drawing_rect:
            # Start drawing rectangle
            self.begin_user_rectangle()

    def mouse_move(self, pos):
        mouse_x, mouse_y = self.get_offset_mouse(pos)
        # Update mouse_grid_position based on current mouse position
        mouse_grid_x, mouse_grid_y = self.get_grid_mouse((mouse_x, mouse_y))
        self.mouse_grid_position = (mouse_grid_x, mouse_grid_y)

        # If mouse_grid position and mouse_prev_grid_position are different
        if (mouse_grid_x, mouse_grid_y) != self.mouse_prev_grid_position:
            self.game.update()

            x_pos = int(self.grid_offset[0] + (mouse_grid_x * self.column_width))
            y_pos = int(self.grid_offset[1] + (mouse_grid_y * self.row_height))

            if not self.drawing_rect:
                pygame.draw.circle(self.game.py_screen, (255, 255, 0), (x_pos, y_pos), 10)
            else:
                origin_x = int(self.grid_offset[0] + (self.rect_origin[0] * self.column_width))
                origin_y = int(self.grid_offset[1] + (self.rect_origin[1] * self.row_height))

                width = x_pos - origin_x
                height = y_pos - origin_y

                pygame.draw.rect(self.game.py_screen, MAROON, (origin_x, origin_y, width, height), 3)

            self.mouse_prev_grid_position = self.mouse_grid_position

class Button():
    def __init__(self, screen, pos, width, height, text, handler):
        self.x = pos[0]
        self.y = pos[1]
        self.game = screen
        self.py_screen = screen.py_screen
        self.text = text
        self.handler = handler

        self.font = pygame.font.Font("resources/Arvo-Regular.ttf", 14)
        self.text_surface = self.font.render(text, True, DARKGREY)
        self.text_pos = self.text_surface.get_rect()

        self.text_pos.x += self.x + 5
        self.text_pos.y += self.y + 5

        self.w = self.text_pos.width + 10
        self.h = self.text_pos.height + 10

        self.rect = pygame.Rect((self.x, self.y), (self.w, self.h))

        RoundedRect(self.py_screen, self.rect, LIGHTGREY)
        self.py_screen.blit(self.text_surface, self.text_pos)

    def is_mouse_over(self, mouse_pos):
        if (mouse_pos[0] >= self.x and
            mouse_pos[0] <= self.x + self.w and
            mouse_pos[1] >= self.y and
            mouse_pos[1] <= self.y + self.h):
            return True
        else:
            return False

    def call(self):
        self.handler()


def RoundedRect(surface, rect, color, radius=0.4):
    """
    RoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = pygame.Rect(rect)
    color        = pygame.Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle       =  pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)

