#####                          #####
#####                          #####
##### Code by tosu_dev at 18yo #####
#####                          #####
#####                          #####


import pygame
from pygame import draw
from pygame.locals import *
import sys
from copy import deepcopy

pygame.init()


# ===== SCREEN =====
SCREEN_SIZE = 900
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Game Life")

# ===== Entry Box ====
class EntryBox:
    """ A box to write in and get the value """
    def __init__(self, name:str, pos:tuple, size:tuple, font_size:int, value:str=""):
        """
        :pos: (x,y)
        :size: (w, h)
        """
        self.name = name
        self.rect = pygame.Rect(pos, size)
        self.is_active = False
        self.bg_color = GRAY
        self.font = pygame.font.SysFont("Consolas", font_size)
        self.value = value

    def active(self):
        self.is_active = True
        self.bg_color = WHITE
    
    def unactive(self):
        self.is_active = False
        self.bg_color = GRAY

    def draw_font(self):
        text = self.font.render(self.value, True, BLACK)
        screen.blit(text, (self.rect.centerx-text.get_width()//2, self.rect.centery-text.get_height()//2))
            

# ===== MAP =====
MAP_SIZE = 10
MAP_SIZE_EXTEND = 50
map = [[0 for _ in range(MAP_SIZE+2*MAP_SIZE_EXTEND)] for __ in range(MAP_SIZE+2*MAP_SIZE_EXTEND)]
map_queue = []
old_map = deepcopy(map)
CELL_SIZE = SCREEN_SIZE//MAP_SIZE


# ===== CLOCK =====
clock = pygame.time.Clock()
TICKS = 10

# ===== COLORS =====
WHITE = (255,255,255)
BLACK = (20,20,20)
GRAY = (200,200,200)
RED = (255,0,0)
GREEN = (0,255,0)
PURPLE = (100,0,100)
CELLS_COLOR = list(WHITE)


# ===== FONTS and OPTIONS =====
def get_entrybox_posx(option_text):
    """ get the x position for an entry box depending of his text option """
    return option_startlinex + option_text.get_width() + option_entryaddx

def get_text_centered(rect, text):
    """ center the text in a rectangle """
    return (rect.centerx-text.get_width()//2, rect.centery-text.get_height()//2)

# GENERATION NUMBER
gen_number_FONT = pygame.font.SysFont("Consolas", 36)
gen_number = 0

# OPTIONS MENU
all_options_entry = []
option_startlinex = 50
option_entryaddx = 25

# Title
option_title_FONT = pygame.font.SysFont("Consolas", 52, bold=True)
option_title_FONT.set_underline(True)
option_title_TEXT = option_title_FONT.render("OPTIONS", True, WHITE)
option_title_POS = (SCREEN_SIZE//2-option_title_TEXT.get_width()//2, option_title_TEXT.get_height()//2)

# Options
option_FONTSIZE = 36
option_FONT = pygame.font.SysFont("Consolas", option_FONTSIZE)
options = {}

def add_option(name:str, text:str, entry_value, previous_option:str=None, pos=None, box_width=80):
    """
    Add an option in the menu of options
    :name: name of the options
    :text: text that will be show on the option menu
    :entry_value: the value of the entry
    :previous_option: the previous option name to calculate the new pos
    :pos: if it is a special pos
    """
    options[name] = {"text": option_FONT.render(text, True, WHITE)}
    if pos:
        options[name]["pos"] = (option_startlinex, pos)
    else:
        options[name]["pos"] = (option_startlinex, options[previous_option]["pos"][1]+2*options[previous_option]["text"].get_height())
    options[name]["entry"] = EntryBox(name,
                                (get_entrybox_posx(options[name]["text"]), options[name]["pos"][1]), 
                                (box_width, options[name]["text"].get_height()), 
                                option_FONTSIZE, value=str(entry_value))
    all_options_entry.append(options[name]["entry"])

# - ticks
add_option("ticks", "- Ticks =", TICKS, pos=option_title_POS[1]+2*option_title_TEXT.get_height())
# - map size
add_option("map", "- Map size =", MAP_SIZE, "ticks")
# - generations
add_option("gen", "- Generation =", gen_number, "map", box_width=110)
# - cells color
add_option("cells-color", "- Cells color = ", str(WHITE)[1:-1], "gen", box_width=300)

# - bottom buttons
option_button_FONT = pygame.font.SysFont("Consolas", 42)
# -- save
option_save_TEXT = option_button_FONT.render("SAVE", True, WHITE)
option_save_BUTTON = pygame.Rect((0, SCREEN_SIZE-80), (150, 80))
option_save_POS = get_text_centered(option_save_BUTTON, option_save_TEXT)
# -- cancel
option_cancel_TEXT = option_button_FONT.render("CANCEL", True, WHITE)
option_cancel_BUTTON = pygame.Rect((option_save_BUTTON.width, SCREEN_SIZE-80), (150, 80))
option_cancel_POS = get_text_centered(option_cancel_BUTTON, option_cancel_TEXT)


# ===== BOOLS =====
EDIDTED_MODE = True
LEFT_CLICK = False
RIGHT_CLICK = False
LEFT_ARROW = False
RIGHT_ARROW = False
PAUSE = True
OPTION = False


# ===== FUNCTIONS =====
def get_nb(i, j):
    """ Get the number of cells around a case at map[i][j] """
    count = 0
    if i <= 0 or j <= 0 or i >= MAP_SIZE+2*MAP_SIZE_EXTEND-1 or j >= MAP_SIZE+2*MAP_SIZE_EXTEND-1:
        raise IndexError

    for line in range(-1, 2):
        for row in range(-1, 2):
            if line == row == 0:
                pass
            elif map[i+line][j+row] == 1:
                count += 1

    return count

def next_gen():
    """ update the map for the next generation """
    global map_queue, old_map, gen_number
    gen_number += 1
    old_map = deepcopy(map)
    map_queue.append(old_map)
    removed_cells = []
    added_cells = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            try:
                nb = get_nb(i, j)
            except:
                nb = 0

            if map[i][j] == 1:
                if nb < 2 or nb > 3:
                    removed_cells.append((i, j))
            else:
                if nb == 3:
                    added_cells.append((i, j))

    for i, j in removed_cells:
        map[i][j] = 0
    
    for i, j in added_cells:
        map[i][j] = 1
    
def draw_map():
    for i in range(MAP_SIZE, MAP_SIZE*2):
        for j in range(MAP_SIZE, MAP_SIZE*2):
            if map[i][j] == 1:
                pygame.draw.rect(screen, CELLS_COLOR, pygame.Rect(((j-MAP_SIZE)*CELL_SIZE, (i-MAP_SIZE)*CELL_SIZE), (CELL_SIZE, CELL_SIZE)))

def show_grid():
    for i in range(len(map)):
        pygame.draw.line(screen, CELLS_COLOR, (0, i*CELL_SIZE), (SCREEN_SIZE, i*CELL_SIZE))
    for j in range(1, len(map[0])):
        pygame.draw.line(screen, CELLS_COLOR, (j*CELL_SIZE, 0), (j*CELL_SIZE, SCREEN_SIZE))

def show_gen_num():
    screen.blit(gen_number_FONT.render(str(gen_number), True, RED), (0,0))

def draw_option(name):
    """
    :name: name of the option
    """
    screen.blit(options[name]["text"], options[name]["pos"])
    pygame.draw.rect(screen, options[name]["entry"].bg_color, options[name]["entry"].rect)
    options[name]["entry"].draw_font()

def option_menu():
    # TITLE
    screen.blit(option_title_TEXT, option_title_POS)

    # OPTIONS
    for option in options:
        draw_option(option)

    # SAVE
    pygame.draw.rect(screen, GREEN, option_save_BUTTON)
    screen.blit(option_save_TEXT, option_save_POS)

    # CANCEL
    pygame.draw.rect(screen, RED, option_cancel_BUTTON)
    screen.blit(option_cancel_TEXT, option_cancel_POS)


while True:
    # ===== EVENT =====
    for event in pygame.event.get():
        # QUIT
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # ===== KEYS =====
        if event.type == KEYDOWN:
            # QUIT
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            if not OPTION:
                # Switch EDITOR MODE
                if event.key == K_RETURN:
                    PAUSE = True
                    EDIDTED_MODE = not EDIDTED_MODE
            
                # Keys in SIMULATION
                if not EDIDTED_MODE:
                    # NAVIGUATE BETWEENS GENS (not in EDITOR)
                    if event.key == K_RIGHT:
                        RIGHT_ARROW = True
                        PAUSE = True
                        next_gen()
                    if event.key == K_LEFT:
                        LEFT_ARROW = True
                        PAUSE = True
                        if len(map_queue) > 0:
                            gen_number -= 1
                            map = deepcopy(map_queue[-1])
                            map_queue.pop()

                    # PAUSE
                    if event.key == K_SPACE:
                        PAUSE = not PAUSE

                # open OPTIONS
                if event.key == K_o:
                    OPTION = True
                    options["gen"]["entry"].value = str(gen_number)
                    default_options = {option_entry.name: option_entry.value for option_entry in all_options_entry}

        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                RIGHT_ARROW = False
            if event.key == K_LEFT:
                LEFT_ARROW = False

        # Events in EDITOR
        if EDIDTED_MODE and not OPTION:
            # MAP EDIT
            if event.type == MOUSEBUTTONDOWN: 
                mouse_pos = list(event.pos)
                if mouse_pos[0] == 0:
                    mouse_pos = 1
                if mouse_pos[1] == 0:
                    mouse_pos[1] = 1
                j = int((MAP_SIZE / (SCREEN_SIZE / mouse_pos[0]))) + MAP_SIZE
                i = int((MAP_SIZE / (SCREEN_SIZE / mouse_pos[1]))) + MAP_SIZE
                if event.button == 1:
                    LEFT_CLICK = True
                    map[i][j] = 1
                if event.button == 3:
                    RIGHT_CLICK = True
                    map[i][j] = 0
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    LEFT_CLICK = False
                if event.button == 3:
                    RIGHT_CLICK = False
            if event.type == MOUSEMOTION:
                mouse_pos = list(event.pos)
                if mouse_pos[0] == 0:
                    mouse_pos[0] = 1
                if mouse_pos[1] == 0:
                    mouse_pos[1] = 1
                j = int((MAP_SIZE / (SCREEN_SIZE / mouse_pos[0]))) + MAP_SIZE
                i = int((MAP_SIZE / (SCREEN_SIZE / mouse_pos[1]))) + MAP_SIZE

                if LEFT_CLICK: 
                    map[i][j] = 1
                if RIGHT_CLICK:
                    map[i][j] = 0

            if event.type == KEYDOWN:
                # RESET
                if event.key == K_BACKSPACE:
                    map = [[0 for _ in range(MAP_SIZE+2*MAP_SIZE_EXTEND)] for __ in range(MAP_SIZE+2*MAP_SIZE_EXTEND)]
                    gen_number = 0
                if event.key == K_SPACE:
                    EDIDTED_MODE = False
                    PAUSE = False

        # Events in OPTIONS
        elif OPTION:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_posx, mouse_posy = event.pos

                    # select the option
                    for option_entry in all_options_entry:
                        if option_entry.rect.collidepoint(mouse_posx, mouse_posy):
                            option_entry.active()
                        else:
                            option_entry.unactive()

                    # save
                    if option_save_BUTTON.collidepoint(mouse_posx, mouse_posy):
                        # - ticks
                        try:
                            assert int(options["ticks"]["entry"].value)
                        except:
                            options["ticks"]["entry"].value = default_options["ticks"]

                        # - map
                        try:
                            if options["map"]["entry"].value != default_options[1]:
                                MAP_SIZE = int(options["map"]["entry"].value)
                                CELL_SIZE = SCREEN_SIZE//MAP_SIZE
                                #old_map = deepcopy(map)
                                map = [[0 for _ in range(MAP_SIZE+2*MAP_SIZE_EXTEND)] for __ in range(MAP_SIZE+2*MAP_SIZE_EXTEND)]
                                gen_number = 0
                                options["gen"]["entry"].value = str(gen_number)
                        except:
                            options["map"]["entry"].value = default_options["map"]

                        # - generation
                        try:
                                if int(options["gen"]["entry"].value) != gen_number:
                                    if int(options["gen"]["entry"].value) < gen_number:
                                        gen_number = int(options["gen"]["entry"].value)
                                        map_queue = map_queue[:gen_number+1]
                                        map = deepcopy(map_queue[-1])
                                    else:
                                        while gen_number < int(options["gen"]["entry"].value):
                                            next_gen()
                        except:
                                    options["gen"]["entry"].value = default_options["gen"]
                        
                        # - cells color
                        try:
                                new_cells_color = list(options["cells-color"]["entry"].value.split(", "))
                                for i in range(len(new_cells_color)):
                                    new_cells_color[i] = int(new_cells_color[i])
                                CELLS_COLOR = new_cells_color
                                if len(CELLS_COLOR) != 3:
                                    raise ValueError
                                for rgb in CELLS_COLOR:
                                    try:
                                        rgb = int(rgb)
                                    except:
                                        raise ValueError
                                    if rgb > 255:
                                        raise ValueError
                        except:
                                new_cells_color = list(default_options["cells-color"].split(", "))
                                for i in range(len(new_cells_color)):
                                    new_cells_color[i] = int(new_cells_color[i])
                                CELLS_COLOR = new_cells_color
                                options["cells-color"]["entry"].value = default_options["cells-color"]
                                    
                        OPTION = False
                        EDIDTED_MODE = True

                    # cancel
                    elif option_cancel_BUTTON.collidepoint(mouse_posx, mouse_posy):
                        for i, option_entry in enumerate(all_options_entry):
                            option_entry.value = default_options[option_entry.name]
                            OPTION = False
                            EDIDTED_MODE = True
                            
            # write the option value
            if event.type == KEYDOWN:

                for option_entry in all_options_entry:
                    if option_entry.is_active:

                        if event.key == K_BACKSPACE:
                            if len(option_entry.value) > 0:
                                option_entry.value = option_entry.value[:-1]
                        else:
                            if option_entry.name == "ticks":
                                if event.unicode in "0123456789" and len(option_entry.value) < 3:
                                    option_entry.value += str(event.unicode)
                            elif option_entry.name == "map":
                                if event.unicode in "0123456789" and len(option_entry.value) < 3:
                                    option_entry.value += str(event.unicode)
                            elif option_entry.name == "gen":
                                if event.unicode in "0123456789" and len(option_entry.value) < 5:
                                    option_entry.value += str(event.unicode)
                            elif option_entry.name == "cells-color":
                                if event.unicode in "0123456789, ":
                                    option_entry.value += str(event.unicode)
                        break


    # ===== DRAW =====
    screen.fill(BLACK)

    # EDIDTED MODE
    if EDIDTED_MODE and not OPTION:
        TICKS = 240
        SIMULATION_TICKS = 0
        draw_map()
        show_grid()
        show_gen_num()

    # OPTION
    elif OPTION:
        SIMULATION_TICKS = 0
        option_menu()
        show_gen_num()

    # SIMULATION
    else:
        TICKS = int(options["ticks"]["entry"].value)
        draw_map()
        show_gen_num()
        if not PAUSE:
            next_gen()
        else:
            # hold left or right
            TICKS = 10
            if RIGHT_ARROW:
                next_gen()
            elif LEFT_ARROW:
                if len(map_queue) > 0:
                    gen_number -= 1
                    map = deepcopy(map_queue[-1])
                    map_queue.pop()
            
    pygame.display.update()
    
    clock.tick(TICKS)
    