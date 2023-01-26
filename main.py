import pygame
import pygame_gui
from pygame_gui.elements import UIVerticalScrollBar
from pygame_gui.windows.ui_file_dialog import UIFileDialog
from pygame.rect import Rect
from chplog import *
from os.path import exists
from datetime import datetime
from useful_functions import *
from pprint import pprint


# Глобальные константы
# цвета
BLACK = (0, 0, 0)
AS_IF_BLACK = (50, 50, 50)
DARK_GREY = (80, 80, 80)
LIGHT_GREY = (128, 128, 128)
AS_IF_WHITE = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
NAVY = (0, 0, 128)
YELLOW = (200, 200, 100)

# частота кадров
FPS = 30

# прочие
c_MAX_FIGURE_TYPES = 32
g_MAX_DIR_COUNT = 8
c_MAX_PLAYER_COUNT = 4
c_TURN_ATTRIBUTES = 8
c_MAX_TURN_PRIOR = 100

c_GAME_STATUS_FINISHED = True


def add_figures_type():
    global g_figure_types
    g_figure_types.append([0, '', 0])
    init_figures_type(len(g_figure_types) - 1)


def init_figures_type(ind):
    global g_figure_types
    g_figure_types[ind][0] = 1  # номер игрока
    g_figure_types[ind][1] = "unknown"  # название фигуры
    g_figure_types[ind][2] = 1  # рисунок


def add_turn():
    global g_turns, c_TURN_ATTRIBUTES
    g_turns.append([[] for _ in range(c_TURN_ATTRIBUTES)])
    init_turns(len(g_turns) - 1)


def init_turns(ind):
    global g_turns
    ## я не сделал всё через генератор списка, чтобы оставить комментарии, по которым я потом смогу понять, что делает эта функция
    g_turns[ind][0] = []  # фигуры, которые могут совершать этот ход
    g_turns[ind][1] = []  # направления, в которых может быть совершён ход
    g_turns[ind][2] = []  # перечисление возможной длины ходов
    g_turns[ind][3] = []  # перечисление типов фигур, которые можно перепрыгивать
    g_turns[ind][4] = []  # перечисление типов фигур, которые можно замещать
    g_turns[ind][5] = []  # список шаблонов выполнения хода
    g_turns[ind][6] = 0  # приоритет данного хода
    g_turns[ind][7] = False  # является ли ход составным



# Глобальные переменные
g_PLAYER_COUNT = 1
g_CURRENT_PLAYER = 1
g_MAX_PRIORITY_TURN = 0

g_game_name = "This game has no name. It will never be the same"
g_CELLS_WIDTH = 8  # ширина игрового поля в клетках
g_CELLS_HEIGHT = 8  # высота игрового поля в клетках
g_SIZE_OF_CELL = 100  # размер одной клетки в пикселях
g_GAME_BOARD_COLOUR = [128, 128, 128]  # Цвет игрового поля (RGB)
g_SECOND_GAME_BOARD_COLOUR = None  # второй цвет игрового поля (если есть)
g_COLORED_TOPLEFT_FL = False  # будет ли закрашена верхняя левая клетка игрового поля
g_WIDTH = g_CELLS_WIDTH * g_SIZE_OF_CELL
g_HEIGHT = g_CELLS_HEIGHT * g_SIZE_OF_CELL
lst_game_board = [[None for _ in range(g_CELLS_WIDTH)] for _ in range(g_CELLS_HEIGHT)]
g_game_status = None  # отвечает за игровой статус. None - не начата; False - начата; True - завершена
g_file_name_rules = ""
g_colored_cells_lst = list()
g_loaded_cells_lst = list()
g_special_cells_lst = list()
g_win_conditions_pos = list()
g_win_conditions_num = list()
g_history_of_a_game = list()  # сюда будут записываться ходы игроков

g_figure_types = list()
g_turns = list()
add_figures_type()

g_modal_window = False
g_file_selection = None

g_showing_whats_new_fl = False


def init_rules():
    """ Возвращает все переменные к стартовым настройкам."""
    global g_game_name, g_CELLS_WIDTH, g_CELLS_HEIGHT, g_SIZE_OF_CELL, g_GAME_BOARD_COLOUR, g_SECOND_GAME_BOARD_COLOUR, g_COLORED_TOPLEFT_FL, \
        g_figure_types, g_WIDTH, g_HEIGHT, lst_game_board, \
        g_turns, g_PLAYER_COUNT, g_CURRENT_PLAYER, g_game_status, g_special_cells_lst, g_win_conditions_pos, g_win_conditions_num, g_MAX_PRIORITY_TURN, \
        g_colored_cells_lst, g_loaded_cells_lst, g_history_of_a_game
    g_game_name = "This game has no name. It will never be the same"
    g_CELLS_WIDTH = 8  # ширина игрового поля в клетках
    g_CELLS_HEIGHT = 8  # высота игрового поля в клетках
    g_SIZE_OF_CELL = 100  # размер одной клетки в пикселях
    g_GAME_BOARD_COLOUR = [128, 128, 128]  # Цвет игрового поля (RGB)
    g_SECOND_GAME_BOARD_COLOUR = None  # второй цвет игрового поля (если есть)
    g_COLORED_TOPLEFT_FL = False  # будет ли закрашена верхняя левая клетка игрового поля
    g_WIDTH = g_CELLS_WIDTH * g_SIZE_OF_CELL
    g_HEIGHT = g_CELLS_HEIGHT * g_SIZE_OF_CELL

    g_figure_types = []
    add_figures_type()

    g_turns = []
    add_turn()

    g_PLAYER_COUNT = 1
    g_CURRENT_PLAYER = 1

    g_MAX_PRIORITY_TURN = 0

    lst_game_board = [[None for _ in range(g_CELLS_WIDTH)] for _ in range(g_CELLS_HEIGHT)]

    g_game_status = None

    g_colored_cells_lst = []
    g_loaded_cells_lst = []

    g_special_cells_lst = []

    g_win_conditions_pos = []
    g_win_conditions_num = []

    g_history_of_a_game = []


pygame.font.init()

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, colour, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, colour)
    ##text_surface.fill((128, 128, 128))
    text_rect = text_surface.get_rect()
    text_rect.x = x
    text_rect.y = y
    #background_surface = pygame.Surface(text_rect.size)
    #background_surface.fill(DARK_GREY)
    #background_surface.set_colorkey(DARK_GREY)
    #surf.blit(background_surface, text_rect)
    surf.blit(text_surface, text_rect)

def read_release_notes_file():
    global to_write_lst
    with open("History of versions 2.txt", 'r') as whats_new_file:
        to_write_lst = whats_new_file.read().split()

def print_whats_new():
    """ Записывает последние изменения из файла в окно изменений."""
    global to_write_lst
    whats_new_window.fill(YELLOW)
    wnw_width = whats_new_window_rect.width
    wnw_height = whats_new_window_rect.height
    draw_text(whats_new_window, "What's new", 30, BLACK, whats_new_window_rect.width // 8, 10)
    pygame.draw.rect(whats_new_window, GREEN, (wnw_width - 20, 0, 20, wnw_height))

    #print(release_notes_bar.rect.topright)

    to_write_x = 10
    to_write_y = 50 + wnw_height - release_notes_bar.rect.top
    to_write_size = 20
    #text_rect_bottomright = text_rect(to_write, to_write_size, to_write_x, to_write_y)
    #print(text_rect_bottomright, whats_new_window_rect.right)
    for i in range(len(to_write_lst)):
            r = to_write_lst[i] + " "
            if text_rect(r, to_write_size, to_write_x, to_write_y)[0] > whats_new_window_rect.width - 20:
                to_write_x = 10
                to_write_y += 25
            #draw_text(term_text_surf, r, to_write_size, BLACK, to_write_x, to_write_y)
            draw_text(whats_new_window, r, to_write_size, BLACK, to_write_x, to_write_y)
            to_write_x = text_rect(r, to_write_size, to_write_x, to_write_y)[0]
        #whats_new_window.blit(term_text_surf, (0, release_notes_bar.rect.y))

def text_rect(text, size, x, y):
    """ Получает на вход текст, вычисляет размеры rect для него и возвращает координаты его правой нижней точки."""
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    ##text_surface.fill((128, 128, 128))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    return text_rect.bottomright

def draw_text_with_word_wrap(to_write_lst, ):  # пока не работает
    for i in range(len(to_write)):
            r = to_write[i] + " "
            if text_rect(r, to_write_size, to_write_x, to_write_y)[0] > whats_new_window_rect.right:
                to_write_x = 10
                to_write_y += 25
            draw_text(whats_new_window, r, to_write_size, BLACK, to_write_x, to_write_y)
            to_write_x = text_rect(r, to_write_size, to_write_x, to_write_y)[0]

def show_whats_new():
    """ При нажатии на кнопку "Updates" появляется или исчезает окно с перечислением последних обновлений."""
    release_notes_bar.scrolling()
    screen.blit(whats_new_window, whats_new_window_rect)
    print_whats_new()


def align(arg):  # Принимает на вход кортеж
    if type(arg) is tuple:  # Если это кортеж или список,
        return arg[0] // g_SIZE_OF_CELL * g_SIZE_OF_CELL + g_SIZE_OF_CELL // 2, arg[1] // g_SIZE_OF_CELL * g_SIZE_OF_CELL + g_SIZE_OF_CELL // 2
    else:
        return arg // g_SIZE_OF_CELL * g_SIZE_OF_CELL + g_SIZE_OF_CELL // 2


def align_const(arg):  # Принимает на вход аргумент
    if type(arg) is tuple:  # Если это кортеж или список,
        return arg[0] // g_SIZE_OF_CELL, arg[1] // g_SIZE_OF_CELL
    else:
        return arg // g_SIZE_OF_CELL


def find_figure_by_coors(coors):
    for fig in all_figures:
        if fig.rect.center == coors:
            return fig


def anti_align_const(arg):
    if type(arg) is tuple:  # Если это кортеж или список,
        return arg[0] * g_SIZE_OF_CELL + g_SIZE_OF_CELL // 2, arg[1]  * g_SIZE_OF_CELL + g_SIZE_OF_CELL // 2
    else:
        return arg * g_SIZE_OF_CELL + g_SIZE_OF_CELL // 2



def print_game_name(txt):
    pygame.draw.rect(interface_screen, WHITE, (96, 16, g_WIDTH - 104, 30))
    pygame.draw.rect(interface_screen, BLUE, (96, 16, g_WIDTH - 104, 30), 2)
    draw_text(interface_screen, "game: " + txt, 24, BLACK, 100, 16)

def print_player_count(txt):
    pygame.draw.rect(interface_screen, WHITE, (96, 47, 118, 30))
    pygame.draw.rect(interface_screen, BLUE, (96, 47, 118, 30), 2)
    draw_text(interface_screen, "players: " + txt, 22, BLACK, 100, 49)

def print_player_move(txt):
    pygame.draw.rect(interface_screen, WHITE, (216, 47, 101, 30))
    pygame.draw.rect(interface_screen, BLUE, (216, 47, 101, 30), 2)
    draw_text(interface_screen, "move: " + txt, 22, BLACK, 220, 49)

def print_game_status(txt):
    pygame.draw.rect(interface_screen, WHITE, (319, 47, g_WIDTH - 327, 30))
    pygame.draw.rect(interface_screen, BLUE, (319, 47, g_WIDTH - 327, 30), 2)
    draw_text(interface_screen, "game status: " + txt, 22, BLACK, 325, 49)

def print_info(txt):
    pygame.draw.rect(interface_screen, WHITE, (96, 78, g_WIDTH - 104, 30))
    pygame.draw.rect(interface_screen, BLUE, (96, 78, g_WIDTH - 104, 30), 2)
    draw_text(interface_screen, "info: " + txt, 22, BLACK, 100, 80)



def load_game_rules(file_name):
    # Возвращает результат выполнения (True, если есть ошибки, False, если их нет)
    global g_file_name_rules, g_game_name, g_CELLS_WIDTH, g_CELLS_HEIGHT, g_SIZE_OF_CELL, \
        g_GAME_BOARD_COLOUR, g_SECOND_GAME_BOARD_COLOUR, g_COLORED_TOPLEFT_FL, \
        g_figure_types, lst_game_board, c_MAX_FIGURE_TYPES, \
        g_PLAYER_COUNT, c_MAX_PLAYER_COUNT, g_win_conditions_pos, c_MAX_TURN_PRIOR
    init_rules()
    file_name = g_file_name_rules
    l_s_source_name = "load_game_rules"
    l_current_figure_type = 0
    l_current_turn = 0
    l_current_winner = 0
    l_error_on_load_fl = False

    stroke.rect.center = (-100, -100)

    if not exists(file_name):  # Если файла не существует
        l_error_on_load_fl = True
        log_write(l_s_source_name, "file " + file_name + " not exists. create empty")
        my_file = open(file_name, 'w')
        my_file.write("File was recreated by error on open for reading")
        my_file.close()

    with open(file_name, 'r') as my_file:
        s = my_file.readlines()
        i_ind_file_string = 0
        while i_ind_file_string < len(s):
            #print(i_ind_file_string)
            file_string = s[i_ind_file_string]
            # отрезаем комменты
            if file_string.find('#') >= 0:
                file_string = file_string[:file_string.find('#')]

            # Заполняем глобальные переменные
            #print('!', file_string, '!')
            if file_string[:9] == "game_name":
                if file_string.find("=") > -1:
                    g_game_name = file_string[file_string.find("=") + 1:50].strip()
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "game_name: '=' absent")

            elif file_string[:11] == "CELLS_WIDTH":
                if file_string.find("=") > -1:
                    if file_string[file_string.find("=") + 1:].strip().isdigit():
                        g_CELLS_WIDTH = int(file_string[file_string.find("=") + 1:])
                        lst_game_board = [[None for _ in range(g_CELLS_WIDTH)] for _ in range(g_CELLS_HEIGHT)]
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "CELLS_WIDTH: no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "CELLS_WIDTH: '=' absent")

            elif file_string[:12] == "CELLS_HEIGHT":
                if file_string.find("=") > -1:
                    if file_string[file_string.find("=") + 1:].strip().isdigit():
                        g_CELLS_HEIGHT = int(file_string[file_string.find("=") + 1:])
                        lst_game_board = [[None for _ in range(g_CELLS_WIDTH)] for _ in range(g_CELLS_HEIGHT)]
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "CELLS_HEIGHT: no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "CELLS_HEIGHT: '=' absent")

            elif file_string[:12] == "SIZE_OF_CELL":
                if file_string.find("=") > -1:
                    if file_string[file_string.find("=") + 1:].strip().isdigit():
                        g_SIZE_OF_CELL = int(file_string[file_string.find("=") + 1:])
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "SIZE_OF_CELL: no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "SIZE_OF_CELL: '=' absent")

            elif file_string[:12] == "GB_COLOR_RED":
                if file_string.find("=") > -1:
                    if file_string[file_string.find("=") + 1:].strip().isdigit():
                        g_GAME_BOARD_COLOUR[0] = int(file_string[file_string.find("=") + 1:])
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "GB_COLOR_RED: no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "GB_COLOR_RED: '=' absent")

            elif file_string[:14] == "GB_COLOR_GREEN":
                if file_string.find("=") > -1:
                    if file_string[file_string.find("=") + 1:].strip().isdigit():
                        g_GAME_BOARD_COLOUR[1] = int(file_string[file_string.find("=") + 1:])
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "GB_COLOR_GREEN: no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "GB_COLOR_GREEN: '=' absent")

            elif file_string[:13] == "GB_COLOR_BLUE":
                if file_string.find("=") > -1:
                    if file_string[file_string.find("=") + 1:].strip().isdigit():
                        g_GAME_BOARD_COLOUR[2] = int(file_string[file_string.find("=") + 1:])
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "GB_COLOR_BLUE: no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "GB_COLOR_BLUE: '=' absent")

            elif file_string[:15] == "GB_SECOND_COLOR":
                g_SECOND_GAME_BOARD_COLOUR = [0, 0, 0]  # если мы обнаруживаем, что у игрового поля будет два цвета, то сразу же подготавливаем для этого
                # нашу глобальную переменную
                # по умолчанию устанавливаем туда чёрный
                if file_string.find("=") > -1:
                    if file_string.find(";") > -1:
                        temp_rap_fs = replace_all_punc(file_string)  # temp replaced-all-punc file_string
                        #print(temp_rap_fs[temp_rap_fs.find("=") + 1: temp_rap_fs.find(";")])
                        if temp_rap_fs[temp_rap_fs.find("=") + 1: temp_rap_fs.find(";")].replace(" ", "").isdigit():
                            term_lst = list(map(int, temp_rap_fs[temp_rap_fs.find("=") + 1: temp_rap_fs.find(";")].strip().split()))
                            for i in range(min(3, len(term_lst))):
                                g_SECOND_GAME_BOARD_COLOUR[i] = term_lst[i]
                            if "TRUE" in file_string.upper():
                                g_COLORED_TOPLEFT_FL = True
                            else:
                                g_COLORED_TOPLEFT_FL = False  ## насчёт false по умолчанию ещё надо будет подумать
                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "GB_SECOND_COLOR: no-numbers found")
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "GB_SECOND_COLOR: ';' absent")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "GB_SECOND_COLOR: '=' absent")


            elif file_string[:12] == "colored_cell":
                if file_string.find("=") > -1:
                    #print(replace_all_punc(file_string).replace(" ", "")[replace_all_punc(file_string).replace(" ", "").index("=") + 1:])
                    #print(replace_all_punc(file_string).replace("-", "").replace(" ", "")[replace_all_punc(file_string)
                                                                                               #.replace("-", "").replace(" ", "")
                                                                                               #.index("=") + 1:].strip().isdigit())
                    if replace_all_punc(file_string).replace(";", "").replace("-", "").replace("_", "").replace(" ", "")[replace_all_punc(file_string)
                               .replace("-", "").replace("_", "").replace(" ", "").index("=") + 1:].strip().isdigit():
                        #print("OK")
                        #print(replace_all_punc(file_string)[file_string.index("=") + 1:])
                        term_lst = list(map(int, all_punc_to_whitespases(file_string)
                                            .replace(";", " ").replace("_", " ")[file_string.index("=") + 1:].split()))
                        term_lst[0] -= 1
                        term_lst[1] -= 1
                        #print(term_lst)
                        if len(term_lst) >= 5:
                            if term_lst[0] > g_CELLS_WIDTH - 1:
                                term_lst[0] = g_CELLS_WIDTH - 1
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "colored_cell: value out of range")
                            elif term_lst[0] < 0:
                                term_lst[0] = 0
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "colored_cell: value out of range")

                            if term_lst[1] > g_CELLS_HEIGHT - 1:
                                term_lst[1] = g_CELLS_HEIGHT
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "colored_cell: value out of range")
                            elif term_lst[1] < 0:
                                term_lst[1] = 0
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "colored_cell: value out of range")

                            if term_lst[2] > 255:
                                term_lst[2] = 255
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "colored_cell: value out of range")
                            elif term_lst[2] < 0:
                                term_lst[2] = 0
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "colored_cell: value out of range")

                            if term_lst[3] > 255:
                                term_lst[3] = 255
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "colored_cell: value out of range")
                            elif term_lst[3] < 0:
                                term_lst[3] = 0
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "colored_cell: value out of range")

                            if term_lst[4] > 255:
                                term_lst[4] = 255
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "colored_cell: value out of range")
                            elif term_lst[4] < 0:
                                term_lst[4] = 0
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "colored_cell: value out of range")

                            #print(term_lst)

                            g_colored_cells_lst.append([g_SIZE_OF_CELL - 2, term_lst[0], term_lst[1], tuple(term_lst[2:5])])
                            #print(g_colored_cells_lst)

                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "colored_cell: incorrect number of values")
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "colored_cell: no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "colored_cell: '=' absent")

            elif file_string[:11] == "loaded_cell":
                if file_string.find("=") > -1:
                    if file_string.count(";") == 1:
                        term_lst = file_string.split(";")
                        #print(term_lst)
                        term_lst[0] = all_punc_to_whitespases(term_lst[0])[all_punc_to_whitespases(term_lst[0]).index("=") + 1:].strip()
                        #print(term_lst[0])
                        if term_lst[0].replace(" ", "").isdigit():
                            #print("OK")
                            term_lst[0] = list(map(int, term_lst[0].split()))
                            if len(term_lst[0]) >= 2:
                                term_lst[0][0] -= 1
                                term_lst[0][1] -= 1
                                if term_lst[0][0] > g_CELLS_WIDTH - 1:
                                    term_lst[0][0] = g_CELLS_WIDTH - 1
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "loaded_cell: value out of range")
                                elif term_lst[0][0] < 0:
                                    term_lst[0][0] = 0
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "loaded_cell: value out of range")

                                if term_lst[0][1] > g_CELLS_HEIGHT - 1:
                                    term_lst[0][1] = g_CELLS_HEIGHT - 1
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "loaded_cell: value out of range")
                                elif term_lst[0][1] < 0:
                                    term_lst[0][1] = 0
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "loaded_cell: value out of range")

                                # coors OK, checking filepath
                                term_lst[-1] = term_lst[-1].replace("(", "").replace(")", "").replace(";", "").replace(":", "").replace("\n", "").strip()
                                if exists(term_lst[-1]):
                                    # filepath OK, appending
                                    g_loaded_cells_lst.append([term_lst[0][0], term_lst[0][1], term_lst[1]])
                                    #print(g_loaded_cells_lst)
                                else:
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "loaded_cell: filepath does not exist")
                            else:
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "loaded_cell: incorrect number of values")
                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "loaded_cell: no-numbers found")
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "loaded_cell: incorrect number of ';' ")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "loaded_cell: '=' absent")

            elif file_string[:11] == "figure_type":
                if file_string.find("=") > -1:
                    if file_string[file_string.find("=") + 1:].strip().isdigit():
                        tft = int(file_string[file_string.find("=") + 1:])
                        if 0 < tft < c_MAX_FIGURE_TYPES + 1:
                            if tft > l_current_figure_type:
                                for _ in range(l_current_figure_type, tft):
                                    add_figures_type()
                            l_current_figure_type = tft
                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "figure_type: number out of range (0, 32)")
                            l_current_figure_type = 1
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "figure_type: no-numbers found")
                        l_current_figure_type = 1
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "figure_type: '=' absent")
                    l_current_figure_type = 1

            elif file_string[:9] == "ft_player":
                if file_string.find("=") > -1:
                    if file_string[file_string.find("=") + 1:].strip().isdigit():
                        g_figure_types[l_current_figure_type][0] = int(file_string[file_string.find("=") + 1:])
                        # обновим число игроков в игре

                        if g_PLAYER_COUNT < int(file_string[file_string.find("=") + 1:]):
                            g_PLAYER_COUNT = int(file_string[file_string.find("=") + 1:])
                        if c_MAX_PLAYER_COUNT < int(file_string[file_string.find("=") + 1:]):
                            g_PLAYER_COUNT = c_MAX_PLAYER_COUNT
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "ft_player:" + file_string + " max player count (" + str(c_MAX_PLAYER_COUNT) + ") exceed")
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "ft_player: no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "ft_player: '=' absent")

            elif file_string[:7] == "ft_name":
                if file_string.find("=") > -1:
                    g_figure_types[l_current_figure_type][1] = file_string[file_string.find("=") + 1:50].strip()
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "ft_name: '=' absent")

            elif file_string[:11] == "ft_img_type":
                if file_string.find("=") > -1:
                    if file_string[file_string.find("=") + 1:].strip().isdigit():
                        g_figure_types[l_current_figure_type][2] = int(file_string[file_string.find("=") + 1:])
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "ft_img_type: no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "ft_img_type: '=' absent")

            elif file_string[:12] == "game_brd_add":
                if file_string.find("=") > -1:
                        l_list = file_string[file_string.find("=") + 1:].replace(' ', '').replace('\n', '')\
                            .replace('(', '').replace(')', '').split(';')
                        for i_ind_gbl in range(len(l_list)):
                            l_list[i_ind_gbl] = l_list[i_ind_gbl].split(',')
                            if len(l_list[i_ind_gbl]) == 3:

                                l_fl = False
                                if l_list[i_ind_gbl][0].isdigit():
                                    if 1 <= int(l_list[i_ind_gbl][0]) <= g_CELLS_WIDTH:
                                        l_list[i_ind_gbl][0] = int(l_list[i_ind_gbl][0])
                                    else:
                                        l_fl = True
                                        l_error_on_load_fl = True
                                        log_write(l_s_source_name, "game_brd_add -" + str(l_list[i_ind_gbl]) + " : value out of range")
                                else:
                                    l_fl = True
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "game_brd_add -" + str(l_list[i_ind_gbl]) + " : no-numbers found")

                                if l_list[i_ind_gbl][1].isdigit():
                                    if 1 <= int(l_list[i_ind_gbl][1]) <= g_CELLS_HEIGHT:
                                        l_list[i_ind_gbl][1] = int(l_list[i_ind_gbl][1])
                                    else:
                                        l_fl = True
                                        l_error_on_load_fl = True
                                        log_write(l_s_source_name, "game_brd_add -" + str(l_list[i_ind_gbl]) + " : value out of range")
                                else:
                                    l_fl = True
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "game_brd_add -" + str(l_list[i_ind_gbl]) + " : no-numbers found")

                                if l_list[i_ind_gbl][2].isdigit():
                                    if 1 <= int(l_list[i_ind_gbl][2]) <= c_MAX_FIGURE_TYPES:
                                        l_list[i_ind_gbl][2] = int(l_list[i_ind_gbl][2])
                                    else:
                                        l_fl = True
                                        l_error_on_load_fl = True
                                        log_write(l_s_source_name, "game_brd_add -" + str(l_list[i_ind_gbl]) + " : value out of range")
                                else:
                                    l_fl = True
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "game_brd_add -" + str(l_list[i_ind_gbl]) + " : no-numbers found")

                            else:
                                l_fl = True
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "game_brd_add: num_of_symbols != 3:" + str(l_list[i_ind_gbl]))

                            if not l_fl:
                                # Ошибок в параметрах фигуры не найдено, рисуем фигуру
                                lst_game_board[l_list[i_ind_gbl][1] - 1][l_list[i_ind_gbl][0] - 1] = l_list[i_ind_gbl][2]

                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "game_brd_add: '=' absent")

            elif file_string[:13] == "gm_brd_sp_add":  # Обработка специальных клеток
                if file_string.find("=") > -1:
                        l_list = file_string[file_string.find("=") + 1:].replace(' ', '').replace('\n', '')\
                            .replace('(', '').replace(')', '').split(';')
                        if len(l_list) == 2:  # если у нас два набора
                            l_list[0] = l_list[0].split(',')
                            l_list[1] = l_list[1].split(',')
                            if (len(l_list[0]) == 3) and (len(l_list[1]) == 3):  # если оба набора состоят из трёх элементов
                                if l_list[0][0].isdigit() and l_list[0][1].isdigit() and l_list[0][1].isdigit() and \
                                     l_list[1][0].isdigit() and l_list[1][1].isdigit() and l_list[1][2].isdigit():  # если они все цифры
                                    if (1 <= int(l_list[0][0]) <= g_CELLS_WIDTH) and (1 <= int(l_list[1][0]) <= g_CELLS_WIDTH) and \
                                        (1 <= int(l_list[0][1]) <= g_CELLS_HEIGHT) and (1 <= int(l_list[1][1]) <= g_CELLS_HEIGHT) and \
                                         (1 <= int(l_list[0][2]) <= c_MAX_FIGURE_TYPES) and (1 <= int(l_list[1][2]) <= c_MAX_FIGURE_TYPES):
                                        l_list[0] = list(map(int, l_list[0]))
                                        l_list[1] = list(map(int, l_list[1]))
                                        g_special_cells_lst.append([])
                                        g_special_cells_lst[-1].append([])
                                        g_special_cells_lst[-1][-1].append(l_list[0][0] - 1)
                                        g_special_cells_lst[-1][-1].append(l_list[0][1] - 1)
                                        g_special_cells_lst[-1][-1].append(l_list[0][2])
                                        g_special_cells_lst[-1].append([])
                                        g_special_cells_lst[-1][-1].append(l_list[1][0] - 1)
                                        g_special_cells_lst[-1][-1].append(l_list[1][1] - 1)
                                        g_special_cells_lst[-1][-1].append(l_list[1][2])
                                    else:
                                        l_error_on_load_fl = True
                                        log_write(l_s_source_name, "gm_brd_sp_add -" + str(l_list[0]) + " : value width out of range")
                                else:
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "gm_brd_sp_add - " + str(l_list) + " : no-numbers found")
                            else:
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "gm_brd_sp_add - " + str(l_list) + " : num of sets is not 3")
                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "gm_brd_sp_add: num of sets is not 2")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "tn_figures: '=' absent")

            elif file_string[:8] == "turn_add":  # Начинаем обработку ходов
                l_current_turn += 1
                add_turn()

            elif file_string[:10] == "tn_figures":
                l_fl = False
                if file_string.find("=") > -1:
                    l_list = file_string[file_string.find("=") + 1:].replace(' ', '').replace('(', '').replace(')', '').replace('\n', '').split(',')
                    for i_ind_tns in range(len(l_list)):
                        if not l_fl:
                            if l_list[i_ind_tns].isdigit():
                                if int(l_list[i_ind_tns]) == 0:
                                    for j_ind_tns in range(1, len(g_figure_types)):
                                        g_turns[l_current_turn][0].append(j_ind_tns)
                                else:
                                    g_turns[l_current_turn][0].append(int(l_list[i_ind_tns]))
                            else:
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "tn_figures - " + str(l_list) + " : no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "tn_figures: '=' absent")

            elif file_string[:10] == "tn_directs":
                if file_string.find("=") > -1:
                    l_list = file_string[file_string.find("=") + 1:].replace(' ', '').replace('(', '').replace(')', '').replace('\n', '').split(',')
                    for i_ind_tns in range(len(l_list)):
                        if l_list[i_ind_tns].isdigit():
                            if int(l_list[i_ind_tns]) == 0:
                                for j_ind_tns in range(g_MAX_DIR_COUNT):
                                    g_turns[l_current_turn][1].append(j_ind_tns + 1)
                            elif 0 < int(l_list[i_ind_tns]) <= g_MAX_DIR_COUNT:
                                g_turns[l_current_turn][1].append(int(l_list[i_ind_tns]))
                            else:
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "tn_directs -" + str(l_list) + " : value out of range")
                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "tn_directs -" + str(l_list) + " : no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "tn_directs: '=' absent")

            elif file_string[:6] == "tn_len":
                if file_string.find("=") > -1:
                    l_list = file_string[file_string.find("=") + 1:].replace(' ', '').replace('(', '').replace(')', '').replace('\n', '').split(',')
                    for i_ind_tns in range(len(l_list)):
                        if l_list[i_ind_tns].isdigit():
                            if int(l_list[i_ind_tns]) == 0:
                                for j_ind_tns in range(max(g_CELLS_HEIGHT, g_CELLS_WIDTH) - 1):
                                    g_turns[l_current_turn][2].append(j_ind_tns + 1)
                            else:
                                g_turns[l_current_turn][2].append(int(l_list[i_ind_tns]))
                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "tn_len - " + str(l_list) + " : no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "tn_len: '=' absent")

            elif file_string[:7] == "tn_jump":
                if file_string.find("=") > -1:
                    l_list = file_string[file_string.find("=") + 1:].replace(' ', '').replace('(', '').replace(')', '').replace('\n', '').split(',')
                    for i_ind_tns in range(len(l_list)):
                        if l_list[i_ind_tns].isdigit():
                            if int(l_list[i_ind_tns]) == 0:
                                for j_ind_tns in range(len(g_figure_types)):
                                    g_turns[l_current_turn][3].append(j_ind_tns + 1)
                            else:
                                g_turns[l_current_turn][3].append(int(l_list[i_ind_tns]))
                        elif l_list[i_ind_tns] == '':
                            #print('void not loaded')
                            l_list[i_ind_tns] = l_list[i_ind_tns]
                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "tn_jump - " + str(l_list) + " : no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "tn_jump: '=' absent")

            elif file_string[:10] == "tn_replace":
                if file_string.find("=") > -1:
                    l_list = file_string[file_string.find("=") + 1:].replace(' ', '').replace('(', '').replace(')', '').replace('\n', '').split(',')
                    for i_ind_tns in range(len(l_list)):
                        if l_list[i_ind_tns].isdigit():
                            if int(l_list[i_ind_tns]) == 0:
                                for j_ind_tns in range(len(g_figure_types)):
                                    g_turns[l_current_turn][4].append(j_ind_tns + 1)
                            else:
                                g_turns[l_current_turn][4].append(int(l_list[i_ind_tns]))
                        elif l_list[i_ind_tns] == '':
                            l_list[i_ind_tns] = l_list[i_ind_tns]
                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "tn_replace - " + str(l_list) + " : no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "tn_replace: '=' absent")

            elif file_string[:9] == "tn_action":
                l_temp_list = []  # временный список
                l_good_action_fl = True  # флаг, обозначающий, есть ли ошибки в actions
                if file_string.find("=") > -1:
                    l_list = file_string[file_string.find("=") + 1:].replace(' ', '').replace('(', '').replace(')', '').replace('\n', '').split(';')
                    #print('1 step:', l_list)
                    if len(l_list) > 2:
                        # шаг 1. Обрабатываем направление
                        l_sub_list = l_list[0].split(',')
                        #print(l_sub_list)
                        l_temp_list.append([])
                        for i_ind_tns in range(len(l_sub_list)):
                            if l_sub_list[i_ind_tns].isdigit():
                                if int(l_sub_list[i_ind_tns]) == 0:
                                    for j_ind_tns in range(g_MAX_DIR_COUNT):
                                        l_temp_list[-1].append(j_ind_tns + 1)
                                elif 0 < int(l_sub_list[i_ind_tns]) <= g_MAX_DIR_COUNT:
                                     l_temp_list[-1].append(int(l_sub_list[i_ind_tns]))
                                else:
                                    l_error_on_load_fl = True
                                    l_good_action_fl = False
                                    log_write(l_s_source_name, "tn_action -" + str(l_list) + " directions value out of range")
                            else:
                                l_error_on_load_fl = True
                                l_good_action_fl = False
                                log_write(l_s_source_name, "tn_action -" + str(l_list) + " directions: no-numbers found")

                        # шаг 2. Обрабатываем шаблоны поиска
                        for i_ind in range(1, len(l_list) - 1):
                            l_temp_list.append([])
                            l_sub_list = l_list[i_ind].split(',')
                            #print('2 step:', l_sub_list)
                            for i_ind_tns in range(len(l_sub_list)):
                                if l_sub_list[i_ind_tns].isdigit():
                                    if int(l_sub_list[i_ind_tns]) == 0:
                                        for j_ind_tns in range(1, len(g_figure_types)):
                                            l_temp_list[-1].append(j_ind_tns)
                                    else:
                                        l_temp_list[-1].append(int(l_sub_list[i_ind_tns]))
                                elif l_sub_list[i_ind_tns] == '':
                                    l_temp_list[-1].append(None)
                                else:
                                    l_error_on_load_fl = True
                                    l_good_action_fl = False
                                    log_write(l_s_source_name, "tn_action -" + str(l_list) + " filter group " + str(i_ind) + " : no-numbers found")

                        # шаг 3. Обрабатываем шаблон применения
                        l_sub_list = l_list[-1].split(',')
                        #print('3 step:', l_sub_list)
                        l_temp_list.append([])
                        for i_ind_tns in range(len(l_sub_list)):
                            for r in l_sub_list[i_ind_tns]:
                                if r.isdigit():
                                    l_temp_list[-1].append(int(r))
                                elif r == '':
                                    #l_temp_list[-1].append('')
                                    r = r
                                else:
                                    l_error_on_load_fl = True
                                    l_good_action_fl = False
                                    log_write(l_s_source_name, "tn_action -" + str(l_list) + " last : not suitable values")

                        # шаг 4. Добавляем или не добавляем весь наш список в g_turns
                        if l_good_action_fl:
                            g_turns[l_current_turn][5].append(l_temp_list)
                            #print('l_temp_list', l_temp_list)
                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "tn_action - " + str(l_list) + " : not loaded")
                    else:
                        if (len(l_list) == 1) and (l_list == ['']):
                            l_error_on_load_fl = l_error_on_load_fl
                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "tn_action - " + file_string + " : too small arguments")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "tn_action: '=' absent")

            elif file_string[:8] == "tn_prior":
                if file_string.find("=") > -1:  # если есть специальный знак - "="
                    if file_string[file_string.find("=") + 1:].replace(' ', '').replace('(', '').replace(')', '').replace('\n', '')\
                            .isdigit():  # если в приоритете записано число
                        cur_turn_prior = int(file_string[file_string.find("=") + 1:])  # в переменной - наш текущий приоритет хода
                        if 0 <= cur_turn_prior <= c_MAX_TURN_PRIOR:  # если он укладывается в рамки допустимых значений
                            g_turns[l_current_turn][6] = cur_turn_prior
                        else:  # а если нет
                            g_turns[l_current_turn][6] = 0  # то присваиваем ему умолчательное значение 1
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "tn_prior : no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "tn_prior: '=' absent")

            elif file_string[:12] == "tn_composite":
                if file_string.find("=") > -1:  # если есть специальный знак - "="
                    value = file_string[file_string.find("=") + 1:].strip().lower()
                    if are_forbidding_words_here(value):
                        g_turns[l_current_turn][7] = False
                    else:
                        g_turns[l_current_turn][7] = True
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "tn_composite: '=' absent")

            elif file_string[:11] == "game_winner":  # добавляет строку с идентификатором игрока,
                # побеждающего при выполнении условий, нижеперечисленных по файлу правил
                if file_string.find("=") > -1:
                    if file_string[file_string.find("=") + 1:].replace(' ', '').replace('\n', '').isdigit():
                        if 0 < int(file_string[file_string.find("=") + 1:].replace(' ', '').replace('\n', '')) <= g_PLAYER_COUNT:
                            l_current_winner = int(file_string[file_string.find("=") + 1:].strip())
                        else:
                            l_error_on_load_fl = True
                            log_write(l_s_source_name, "game_winner: player count value out of range")
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "game_winner: no-numbers found")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "game_winner: '=' absent")

            elif file_string[:12] == "win_cond_pos":
                if l_current_winner != 0:
                    if file_string.find("=") > -1:
                        l_fl = False  # фиксируем корректность набора для регистрации условий позиционной победы во всей строке
                        l_list = file_string[file_string.find("=") + 1:]\
                           .replace(' ', '').replace('(', '').replace(')', '').replace('\n', '').split(';')
                        for i_ind_gbl in range(len(l_list)):
                            l_list[i_ind_gbl] = l_list[i_ind_gbl].split(',')
                            if len(l_list[i_ind_gbl]) == 3:
                                if l_list[i_ind_gbl][0].isdigit():
                                    if 1 <= int(l_list[i_ind_gbl][0]) <= g_CELLS_WIDTH:
                                        l_list[i_ind_gbl][0] = int(l_list[i_ind_gbl][0]) - 1
                                    else:
                                        l_fl = True
                                        l_error_on_load_fl = True
                                        log_write(l_s_source_name, "win_cond_pos - " + str(l_list[i_ind_gbl]) + " : value out of range")
                                else:
                                    l_fl = True
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "win_cond_pos - " + str(l_list[i_ind_gbl]) + " : no-numbers found")

                                if l_list[i_ind_gbl][1].isdigit():
                                    if 1 <= int(l_list[i_ind_gbl][1]) <= g_CELLS_HEIGHT:
                                        l_list[i_ind_gbl][1] = int(l_list[i_ind_gbl][1]) - 1
                                    else:
                                        l_fl = True
                                        l_error_on_load_fl = True
                                        log_write(l_s_source_name, "win_cond_pos - " + str(l_list[i_ind_gbl]) + " : value out of range")
                                else:
                                    l_fl = True
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "win_cond_pos - " + str(l_list[i_ind_gbl]) + " : no-numbers found")

                                if l_list[i_ind_gbl][2].isdigit():
                                    if 0 < int(l_list[i_ind_gbl][2]) < len(g_figure_types):
                                        l_list[i_ind_gbl][2] = int(l_list[i_ind_gbl][2])
                                    else:
                                        l_fl = True
                                        l_error_on_load_fl = True
                                        log_write(l_s_source_name, "win_cond_pos - " + str(l_list[i_ind_gbl]) + " : value out of range")
                                else:
                                    l_fl = True
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "win_cond_pos - " + str(l_list[i_ind_gbl]) + " : no-numbers found")

                            else:
                                l_fl = True
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "win_cond_pos: num_of_symbols != 3:" + str(l_list[i_ind_gbl]))

                        if not l_fl:
                            # Ошибок в параметрах в строке не найдено, добавляем условие
                            l_list.insert(0, l_current_winner)
                            g_win_conditions_pos.append(l_list)
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "win_cond_pos: '=' absent")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "win_cond_pos: winner number is undefined. " + file_string + " ignored")

            elif file_string[:12] == "win_cond_num":
                if l_current_winner != 0:
                    if file_string.find("=") > -1:
                        l_fl = False  # фиксируем корректность набора для регистрации условий позиционной победы во всей строке
                        l_list = file_string[file_string.find("=") + 1:]\
                            .replace(' ', '').replace('(', '').replace(')', '').replace('\n', '').split(';')
                        for i_ind_gbl in range(len(l_list)):
                            l_list[i_ind_gbl] = l_list[i_ind_gbl].split(',')
                            if len(l_list[i_ind_gbl]) == 2:
                                if l_list[i_ind_gbl][0].isdigit():
                                    if 0 < int(l_list[i_ind_gbl][0]) < len(g_figure_types):
                                        l_list[i_ind_gbl][0] = int(l_list[i_ind_gbl][0])
                                    else:
                                        l_fl = True
                                        l_error_on_load_fl = True
                                        log_write(l_s_source_name, "win_cond_num - " + str(l_list[i_ind_gbl]) + " : value out of range")
                                else:
                                    l_fl = True
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "win_cond_num - " + str(l_list[i_ind_gbl]) + " : no-numbers found")

                                if l_list[i_ind_gbl][1].isdigit():
                                    if 0 <= int(l_list[i_ind_gbl][1]) <= g_CELLS_WIDTH * g_CELLS_HEIGHT:
                                        l_list[i_ind_gbl][1] = int(l_list[i_ind_gbl][1])
                                    else:
                                        l_fl = True
                                        l_error_on_load_fl = True
                                        log_write(l_s_source_name, "win_cond_num - " + str(l_list[i_ind_gbl]) + " : value out of range")
                                else:
                                    l_fl = True
                                    l_error_on_load_fl = True
                                    log_write(l_s_source_name, "win_cond_num - " + str(l_list[i_ind_gbl]) + " : no-numbers found")
                            else:
                                l_fl = True
                                l_error_on_load_fl = True
                                log_write(l_s_source_name, "win_cond_num: num_of_symbols != 2:" + str(l_list[i_ind_gbl]))

                        if not l_fl:
                            # Ошибок в параметрах в строке не найдено, добавляем условие
                            l_list.insert(0, l_current_winner)
                            g_win_conditions_num.append(l_list)
                    else:
                        l_error_on_load_fl = True
                        log_write(l_s_source_name, "win_cond_num: '=' absent")
                else:
                    l_error_on_load_fl = True
                    log_write(l_s_source_name, "win_cond_num: winner number is undefined. " + file_string + " ignored")


            i_ind_file_string += 1
        #for ggg in g_turns: print('g_turns', ggg)
        #for ggg in lst_game_board: print('g_brd', ggg)
        #for ggg in g_figure_types: print('g_figure_types', ggg)
    #for ggg in lst_game_board: print('g_brd', ggg)
    #for ggg in g_win_conditions_pos: print('pos', ggg)
    #for ggg in g_win_conditions_num: print('num', ggg)

    return l_error_on_load_fl


class Figure(pygame.sprite.Sprite):
    Type_int = 0
    player_num = None
    can_move = True
    in_composite_turn = False

    def __init__(self, x, y, type_of_figure):  # х и у задаются в размерности lst_game_board
# 1 - чёрный квадрат
# 2 - чёрный круг
# 3 - белый квадрат
# 4 - белый круг
# 5 - красный квадрат
# 6 - красный круг
# 7 - зелёный квадрат
# 8 - зелёный круг
        self.Type_int = type_of_figure
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((g_SIZE_OF_CELL, g_SIZE_OF_CELL))
        self.image.fill(LIGHT_GREY)
        self.image.set_colorkey(LIGHT_GREY)
        img_type = g_figure_types[type_of_figure][2]
        if img_type == 1:
            pygame.draw.polygon(self.image, BLACK, [[g_SIZE_OF_CELL*0.1, g_SIZE_OF_CELL*0.1], [g_SIZE_OF_CELL*0.1, g_SIZE_OF_CELL*0.9],
                                                    [g_SIZE_OF_CELL*0.9, g_SIZE_OF_CELL*0.9], [g_SIZE_OF_CELL*0.9, g_SIZE_OF_CELL*0.1]])
        elif img_type == 2:
            pygame.draw.circle(self.image, BLACK, (g_SIZE_OF_CELL // 2, g_SIZE_OF_CELL // 2), g_SIZE_OF_CELL * 0.4)
        elif img_type == 3:
            pygame.draw.polygon(self.image, WHITE, [[g_SIZE_OF_CELL*0.1, g_SIZE_OF_CELL*0.1], [g_SIZE_OF_CELL*0.1, g_SIZE_OF_CELL*0.9],
                                                    [g_SIZE_OF_CELL*0.9, g_SIZE_OF_CELL*0.9], [g_SIZE_OF_CELL*0.9, g_SIZE_OF_CELL*0.1]])
        elif img_type == 4:
            pygame.draw.circle(self.image, WHITE, (g_SIZE_OF_CELL // 2, g_SIZE_OF_CELL // 2), g_SIZE_OF_CELL * 0.4)
        elif img_type == 5:
            pygame.draw.polygon(self.image, RED, [[g_SIZE_OF_CELL*0.1, g_SIZE_OF_CELL*0.1], [g_SIZE_OF_CELL*0.1, g_SIZE_OF_CELL*0.9],
                                                  [g_SIZE_OF_CELL*0.9, g_SIZE_OF_CELL*0.9], [g_SIZE_OF_CELL*0.9, g_SIZE_OF_CELL*0.1]])
        elif img_type == 6:
            pygame.draw.circle(self.image, RED, (g_SIZE_OF_CELL // 2, g_SIZE_OF_CELL // 2), g_SIZE_OF_CELL * 0.4)
        elif img_type == 7:
            pygame.draw.polygon(self.image, GREEN, [[g_SIZE_OF_CELL*0.1, g_SIZE_OF_CELL*0.1], [g_SIZE_OF_CELL*0.1, g_SIZE_OF_CELL*0.9],
                                                    [g_SIZE_OF_CELL*0.9, g_SIZE_OF_CELL*0.9], [g_SIZE_OF_CELL*0.9, g_SIZE_OF_CELL*0.1]])
        elif img_type == 8:
            pygame.draw.circle(self.image, GREEN, (g_SIZE_OF_CELL // 2, g_SIZE_OF_CELL // 2), g_SIZE_OF_CELL * 0.4)
        else:
            pygame.draw.line(self.image, BLUE, [g_SIZE_OF_CELL*0.1, g_SIZE_OF_CELL*0.1], [g_SIZE_OF_CELL*0.9, g_SIZE_OF_CELL*0.9], 4)
            pygame.draw.line(self.image, BLUE, [g_SIZE_OF_CELL*0.9, g_SIZE_OF_CELL*0.1], [g_SIZE_OF_CELL*0.1, g_SIZE_OF_CELL*0.9], 4)
        self.rect = self.image.get_rect()
        self.rect.center = (x * g_SIZE_OF_CELL + g_SIZE_OF_CELL // 2, y * g_SIZE_OF_CELL + g_SIZE_OF_CELL // 2)

        self.player_num = g_figure_types[type_of_figure][0]
        #lst_game_board[y][x] = self.side

    def movement(self, coors):  # принимает на вход координаты destination на поле в виде котрежа

        if lst_game_board[align_const(coors[1])][align_const(coors[0])] is not None:  # если клетка, на которую мы встаём, не пустая
            find_figure_by_coors(align(coors)).kill()

        # Делаем значение клетки, на которую мы встали, занятым:
        lst_game_board[align_const(coors[1])][align_const(coors[0])] = lst_game_board[align_const(self.rect.centery)][align_const(self.rect.centerx)]
        # Делаем значение клетки, с которой мы ушли, пустым:
        lst_game_board[align_const(self.rect.centery)][align_const(self.rect.centerx)] = None
        self.rect.center = align(coors)  # Собственно, перемещение


class VerticalBorder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, g_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class HorizontalBorder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((g_WIDTH, 2))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class ColoredCell(pygame.sprite.Sprite):
    def __init__(self, size, pos_x, pos_y, colour):  # pos_х и pos_у задаются в размерности lst_game_board
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.center = ((pos_x + 0.5) * g_SIZE_OF_CELL, (pos_y + 0.5) * g_SIZE_OF_CELL)
        all_sprites.add(self)


class LoadedCell(pygame.sprite.Sprite):  # pos_х и pos_у задаются в размерности lst_game_board
    def __init__(self, pos_x, pos_y, filepath):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filepath)
        self.image = pygame.transform.scale(self.image, (g_SIZE_OF_CELL - 2, g_SIZE_OF_CELL - 2))
        self.rect = self.image.get_rect()
        self.rect.center = ((pos_x + 0.5) * g_SIZE_OF_CELL, (pos_y + 0.5) * g_SIZE_OF_CELL)
        all_sprites.add(self)


class Stroke(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((g_SIZE_OF_CELL, g_SIZE_OF_CELL))
        self.image.fill(LIGHT_GREY)
        self.image.set_colorkey(LIGHT_GREY)
        pygame.draw.polygon(self.image, YELLOW, [[g_SIZE_OF_CELL*0.05, g_SIZE_OF_CELL*0.05], [g_SIZE_OF_CELL*0.95, g_SIZE_OF_CELL*0.05],
                                                 [g_SIZE_OF_CELL*0.95, g_SIZE_OF_CELL*0.95], [g_SIZE_OF_CELL*0.05, g_SIZE_OF_CELL*0.95]], 4)
        self.rect = self.image.get_rect()
        self.rect.center = (-x, -y)


class Button(pygame.sprite.Sprite):
    Name = ""

    def __init__(self, x, y, size, name):
        self.Name = name
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(WHITE)
        #pygame.draw.polygon(self.image, BLUE, [[-2, -2], [size[0], -2], [size[0], size[1]], [-2, size[1]]], 4)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def on_button_new_click(self):
        global g_file_name_rules, manager, g_modal_window, g_file_selection, whats_new_window, g_WIDTH, g_HEIGHT, g_showing_whats_new_fl

        if self.Name == "button_load":
            open_file_dialog_window()

        elif self.Name == "button_new":
            if g_file_name_rules:
                if load_game_rules(g_file_name_rules):
                    print_info("Error during loading rules from " + str(g_file_name_rules) + ". Check log")
            else:
                init_rules()
            game_board_clear()
            game_board_loading()
            print_info("Game " + g_file_name_rules + " refreshed")
            print_game_name(str(g_game_name))
            print_game_status("")
            print_player_count(str(g_PLAYER_COUNT))
            print_player_move(str(g_CURRENT_PLAYER))

        elif self.Name == "button_release_notes":
            g_showing_whats_new_fl = not g_showing_whats_new_fl


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((g_SIZE_OF_CELL * 0.5, g_SIZE_OF_CELL * 0.5))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, DARK_GREY, (g_SIZE_OF_CELL * 0.25, g_SIZE_OF_CELL * 0.25), g_SIZE_OF_CELL * 0.25)
        self.rect = self.image.get_rect()
        self.rect.center = ((x + 0.5) * g_SIZE_OF_CELL, (y + 0.5) * g_SIZE_OF_CELL)
        all_sprites.add(self)
        points.add(self)


class Scrollbar(pygame.sprite.Sprite):
    pressed_y = 0  # возможно, не понадобится

    def __init__(self, width, height, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        scrollers.add(self)

    def scrolling(self):
        mouse_pressed_fl = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        #print(mouse_pressed_fl, self.rect.topleft, self.rect.bottomright, " ", mouse_pos)
        if self.rect.collidepoint(mouse_pos) and mouse_pressed_fl:
            #print("scrolling")
            self.rect.centery = mouse_pos[1]
            if self.rect.bottom > whats_new_window_rect.bottom:
                self.rect.bottom = whats_new_window_rect.bottom
            if self.rect.top < whats_new_window_rect.top:
                self.rect.top = whats_new_window_rect.top
            self.image.fill(RED)
        else:
            self.image.fill(BLUE)
        #print(self.rect.x - (g_WIDTH - whats_new_window_rect.width) // 2,
                               #self.rect.y - (g_HEIGHT - whats_new_window_rect.height) // 2)
        whats_new_window.blit(self.image,
                              (self.rect.x - (g_WIDTH - whats_new_window_rect.width) // 2,
                               self.rect.y - (g_HEIGHT - whats_new_window_rect.height) // 2))

    def where_pressed(self, coor_y):  # возможно, не понадобится
        self.pressed_y = coor_y



def open_file_dialog_window():
    global g_modal_window, g_file_selection

    rect1 = Rect(0, 0, 300, 300)
    g_modal_window = True
    g_file_selection = UIFileDialog(rect=rect1, manager=manager, allow_picking_directories=False)

    #print(g_file_selection.current_file_path)
    #g_modal_window = False



def is_turn_possible_f(source_figure, destination_pos_gbl):  # получает на вход кортежи координат начальной и конечной ячеек (0 - х, 1 - у)
    # проверяет возможность совершения хода из source_pos_gbl в destination_pos_gbl
    global g_turns, lst_game_board
    xs = align_const(source_figure.rect.center[0])
    ys = align_const(source_figure.rect.center[1])
    xd = destination_pos_gbl[0]
    yd = destination_pos_gbl[1]
    l_move_dir = 0
    l_move_len = 0
    middle_figures = []
    l_for_replace = None

    # определяем направление
    # 1 - пр верх, 2 - право, 3 - пр низ, 4 - низ, 5 - л низ, 6 - лево, 7 - л верх, 8 - верх, 0 - без ограничений
    if (xs < xd) and (ys > yd) and (abs(xd - xs) == abs(yd - ys)):  # пр верх
        l_move_dir = 1
    elif (xs < xd) and (ys == yd):  # право
        l_move_dir = 2
    elif (xs < xd) and (ys < yd) and (abs(xd - xs) == abs(yd - ys)):  # пр низ
        l_move_dir = 3
    elif (xs == xd) and (ys < yd):  # вниз
        l_move_dir = 4
    elif (xs > xd) and (ys < yd) and (abs(xd - xs) == abs(yd - ys)):  # л низ
        l_move_dir = 5
    elif (xs > xd) and (ys == yd):  # влево
        l_move_dir = 6
    elif (xs > xd) and (ys > yd) and (abs(xd - xs) == abs(yd - ys)):  # л верх
        l_move_dir = 7
    elif (xs == xd) and (ys > yd):  # вверх
        l_move_dir = 8
    else:
        l_move_dir = 9  # не стандарт

    # определяем длину
    l_move_len = max(abs(xd - xs), abs(yd - ys))
    #print("dir =", l_move_dir, "len =", l_move_len)


    # собираем список перепрыгнутых фигур для проверки
    d_x = 0
    d_y = 0
    if l_move_len > 1:
        for i_loc in range(1, l_move_len):
            if l_move_dir in {1, 3, 5, 7}:
                d_x = i_loc
                d_y = i_loc
            if l_move_dir in {2, 6}:
                d_x = i_loc
                d_y = 0
            if l_move_dir in {4, 8}:
                d_x = 0
                d_y = i_loc
            if lst_game_board[min(ys, yd) + d_y][min(xs, xd) + d_x] is not None:
                middle_figures.append(lst_game_board[min(ys, yd) + d_y][min(xs, xd) + d_x])

    # определяем тип destination для проверки замены
    #l_for_replace = lst_game_board[yd][xd]

    # let's check
    move_res = None
    for i_loc in range(len(g_turns)):
        k = g_turns[i_loc]
        # проверяем, что правило применимо к source-фигуре
        if lst_game_board[ys][xs] in k[0]:
            #print("source OK")
            # checking directions
            if l_move_dir in k[1]:
                #print("dir OK")
                # checking length
                if l_move_len in k[2]:
                    #print("len OK")
                    #print("middle_figures = ", middle_figures)
                    # checking jumps
                    l_jump_fl = True
                    if len(middle_figures) == 0 and len(k[3]):
                        l_jump_fl = False
                    else:
                        for k1 in middle_figures:
                            if k1 not in k[3]:
                                l_jump_fl = False
                    if l_jump_fl:
                        #print("jump OK")
                        # checking replace
                        if (lst_game_board[yd][xd] is None) or (lst_game_board[yd][xd] in k[4]):
                                #print("replace OK")
                              if not source_figure.in_composite_turn or k[7]:  # если фигура не в составном ходу, или этот ход может быть частью составного
                                    #print("check for the composite turn")
                                    move_res = i_loc
                                    break

    return move_res


def is_any_turns_f(player_num):
    # проверяет возможность совершения хода любой из фигур переданного игрока:
    # True, если есть хоть какой-нибудь ход, False, если никаких возможных ходов нет
    print_info("checking movement for player " + str(player_num) + "...")
    l_res_fl = False

    for fig in all_figures:
                if fig.player_num == player_num:
                    for y_des in range(len(lst_game_board)):
                        for x_des in range(len(lst_game_board[y_des])):
                            #print(x_des, y_des)
                            if (align_const(fig.rect.centerx) != x_des) or (align_const(fig.rect.centery) != y_des):
                                if is_turn_possible_f(fig, (x_des, y_des)) is not None:
                                    l_res_fl = True

    if l_res_fl:
        print_info("check movement for player " + str(player_num) + " - Ok")
    else:
        print_info("check movement for player " + str(player_num) + " - not good")
    return l_res_fl


def is_turn_possible(source_pos_gbl, destination_pos_gbl):  # получает на вход кортежи координат начальной и конечной ячеек (0 - х, 1 - у)
    # проверяет возможность совершения хода из source_pos_gbl в destination_pos_gbl
    global g_turns, lst_game_board
    xs = source_pos_gbl[0]
    ys = source_pos_gbl[1]
    xd = destination_pos_gbl[0]
    yd = destination_pos_gbl[1]
    l_move_dir = 0
    l_move_len = 0
    middle_figures = []
    l_for_replace = None
    # определяем направление
    # 1 - пр верх, 2 - право, 3 - пр низ, 4 - низ, 5 - л низ, 6 - лево, 7 - л верх, 8 - верх, 0 - без ограничений
    if (xs < xd) and (ys > yd) and (abs(xd - xs) == abs(yd - ys)):  # пр верх
        l_move_dir = 1
    elif (xs < xd) and (ys == yd):  # право
        l_move_dir = 2
    elif (xs < xd) and (ys < yd) and (abs(xd - xs) == abs(yd - ys)):  # пр низ
        l_move_dir = 3
    elif (xs == xd) and (ys < yd):  # вниз
        l_move_dir = 4
    elif (xs > xd) and (ys < yd) and (abs(xd - xs) == abs(yd - ys)):  # л низ
        l_move_dir = 5
    elif (xs > xd) and (ys == yd):  # влево
        l_move_dir = 6
    elif (xs > xd) and (ys > yd) and (abs(xd - xs) == abs(yd - ys)):  # л верх
        l_move_dir = 7
    elif (xs == xd) and (ys > yd):  # вверх
        l_move_dir = 8
    else:
        l_move_dir = 9  # не стандарт

    # определяем длину
    l_move_len = max(abs(xd - xs), abs(yd - ys))
    #print("dir =", l_move_dir, "len =", l_move_len)


    # собираем список перепрыгнутых фигур для проверки
    d_x = 0
    d_y = 0
    if l_move_len > 1:
        for i_loc in range(1, l_move_len):
            if l_move_dir in {1, 3, 5, 7}:
                d_x = i_loc
                d_y = i_loc
            if l_move_dir in {2, 6}:
                d_x = i_loc
                d_y = 0
            if l_move_dir in {4, 8}:
                d_x = 0
                d_y = i_loc
            if lst_game_board[min(ys, yd) + d_y][min(xs, xd) + d_x] is not None:
                middle_figures.append(lst_game_board[min(ys, yd) + d_y][min(xs, xd) + d_x])

    # определяем тип destination для проверки замены
    #l_for_replace = lst_game_board[yd][xd]

    # let's check
    move_res = None
    for i_loc in range(len(g_turns)):
        k = g_turns[i_loc]
        # проверяем, что правило применимо к source-фигуре
        if lst_game_board[ys][xs] in k[0]:
            #print("source OK")
            # checking directions
            if l_move_dir in k[1]:
                #print("dir OK")
                # checking length
                if l_move_len in k[2]:
                    #print("len OK")
                    #print("middle_figures = ", middle_figures)
                    # checking jumps
                    l_jump_fl = True
                    if len(middle_figures) == 0 and len(k[3]):
                        l_jump_fl = False
                    else:
                        for k1 in middle_figures:
                            if k1 not in k[3]:
                                l_jump_fl = False
                    if l_jump_fl:
                        #print("jump OK")
                        # checking replace
                        if lst_game_board[yd][xd] is not None:
                            if lst_game_board[yd][xd] in k[4]:
                                #print("replace OK")
                                move_res = i_loc
                                break
                        else:
                            #print("replace OK")
                            move_res = i_loc
                            break

    return move_res


def is_any_turns(player_num):
    # проверяет возможность совершения хода любой из фигур переданного игрока:
    # True, если есть хоть какой-нибудь ход, False, если никаких возможных ходов нет
    print_info("checking movement for player " + str(player_num) + "...")
    l_res_fl = False

    for y_sor in range(len(lst_game_board)):
        for x_sor in range(len(lst_game_board[y_sor])):
            if lst_game_board[y_sor][x_sor] is not None:
                if g_figure_types[lst_game_board[y_sor][x_sor]][0] == player_num:
                    #print(x_sor, y_sor)
                    for y_des in range(len(lst_game_board)):
                        for x_des in range(len(lst_game_board[y_des])):
                            #print(x_des, y_des)
                            if (x_sor != x_des) or (y_sor != y_des):
                                if is_turn_possible((x_sor, y_sor), (x_des, y_des)) is not None:
                                    l_res_fl = True

    if l_res_fl:
        print_info("check movement for player " + str(player_num) + " - Ok")
    else:
        print_info("check movement for player " + str(player_num) + " - not good")
    return l_res_fl


def max_priority_turn_f(figure):
    coors = figure.rect.center
    cur_max_prior = 0

    for j in range(len(lst_game_board)):
        for i in range(len(lst_game_board[j])):
            if is_turn_possible(align_const(coors), (i, j)) is not None:
                if cur_max_prior < g_turns[is_turn_possible(align_const(coors), (i, j))][6]:
                    cur_max_prior = g_turns[is_turn_possible(align_const(coors), (i, j))][6]
    return cur_max_prior


def max_priority_turn(coors):
    """ Функция находит приоритет хода с максимальным приоритетом из возможных для данной фигуры."""
    cur_max_prior = 0
    for j in range(len(lst_game_board)):
        for i in range(len(lst_game_board[j])):
            if is_turn_possible(align_const(coors), (i, j)) is not None:
                if cur_max_prior < g_turns[is_turn_possible(align_const(coors), (i, j))][6]:
                    cur_max_prior = g_turns[is_turn_possible(align_const(coors), (i, j))][6]
    return cur_max_prior


def abs_max_priority_turn():
    """ Функция находит максимальный приоритет хода для ходящего игрока."""
    global lst_game_board, g_figure_types, g_MAX_PRIORITY_TURN
    g_MAX_PRIORITY_TURN = 0
    for fig in all_figures:
        if g_figure_types[lst_game_board[align_const(fig.rect.centery)][align_const(fig.rect.centerx)]][0] == g_CURRENT_PLAYER:
            # иными словами, если мы выбрали фигуру того игрока, который сейчас ходит, то
            if g_MAX_PRIORITY_TURN < max_priority_turn(fig.rect.center):
                g_MAX_PRIORITY_TURN = max_priority_turn(fig.rect.center)


def is_game_finished():
    # проверяет, не завершена ли игра в соответствии с установленными правилами
    # если не найдено ни одного полного условия, при котором игра заканчивается, возвращает 0
    # если хотя бы одно полное условие найдено, возвращает номер игрока, записанного в нём победителем
    l_res_int = 0
    for l_cond in g_win_conditions_pos:
        l_match_fl = True
        for l_cond_1 in l_cond[1:]:
            if lst_game_board[l_cond_1[1]][l_cond_1[0]] != l_cond_1[2]:
                l_match_fl = False
        if l_match_fl is True:
            l_res_int = l_cond[0]

    if l_res_int == 0:  # если после позиционных проверок игра не окончена, то
        l_fig_dict = dict()
        for i_loc in range(len(g_figure_types)):
            l_fig_dict[i_loc] = 0
        for l_row in lst_game_board:
            for l_elem in l_row:
                if l_elem is not None:
                    l_fig_dict[l_elem] += 1
        for l_cond in g_win_conditions_num:
            l_match_fl = True
            for l_cond_1 in l_cond[1:]:
                if l_fig_dict[l_cond_1[0]] != l_cond_1[1]:
                    l_match_fl = False
            if l_match_fl is True:
                l_res_int = l_cond[0]
    #for ggg in g_win_conditions_num:print('num', ggg)
    return l_res_int


def check_table_field(event):
    """ Проверяет, к какой части поля относятся координаты мышки: к игровому полю (возвращает 0) или к интерфейсу (возвр. 1)"""
    l_res = 0
    if event.pos[1] >= g_HEIGHT:
        l_res = 1
    else:
        l_res = 0
    return l_res


def game_board_loading():
    """ Создание и покраска игрового поля, расстановка фигур """
    global screen, g_WIDTH, g_HEIGHT, g_CELLS_WIDTH, g_CELLS_HEIGHT, g_SIZE_OF_CELL, lst_game_board, stroke, interface_screen

    g_WIDTH = g_CELLS_WIDTH * g_SIZE_OF_CELL
    g_HEIGHT = g_CELLS_HEIGHT * g_SIZE_OF_CELL
    screen = pygame.display.set_mode((g_WIDTH, g_HEIGHT + 150))
    interface_screen = pygame.Surface((g_WIDTH, 150))
    interface_screen.fill(DARK_GREY)
    pygame.draw.line(interface_screen, BLACK, [0, 5], [g_WIDTH, 5], 10)
    pygame.display.set_caption(g_game_name)

    # создаём границы
    for i in range(0, g_CELLS_WIDTH + 1):
        v_border = VerticalBorder(i * g_SIZE_OF_CELL, g_HEIGHT // 2)
        borders.add(v_border)
        all_sprites.add(v_border)

    for i in range(0, g_CELLS_HEIGHT + 1):
        h_border = HorizontalBorder(g_WIDTH // 2, i * g_SIZE_OF_CELL)
        borders.add(h_border)
        all_sprites.add(h_border)

    # создаём фигуры
    for j in range(len(lst_game_board)):
        for i in range(len(lst_game_board[j])):  # перебираем координаты каждой фигуры, которую нам предстоит разместить на игровом поле
            if type(lst_game_board[j][i]) is int:
                figure = Figure(i, j, lst_game_board[j][i])
                all_figures.add(figure)
                all_sprites.add(figure)

    update_which_figures_can_move()

    # создаём покрашенные клетки игрового поля
    if g_SECOND_GAME_BOARD_COLOUR is not None:
        for j in range(g_CELLS_HEIGHT):
            for i in range((j % 2 == 0) != g_COLORED_TOPLEFT_FL, g_CELLS_WIDTH, 2):
                cell = ColoredCell(g_SIZE_OF_CELL - 2, i, j, g_SECOND_GAME_BOARD_COLOUR)
                drawn_two_color_cells.add(cell)
    for cs_lst in g_colored_cells_lst:
        cell = ColoredCell(cs_lst[0], cs_lst[1], cs_lst[2], cs_lst[3])
        drawn_colored_cells.add(cell)
    for ls_lst in g_loaded_cells_lst:
        cell = LoadedCell(ls_lst[0], ls_lst[1], ls_lst[2])
        drawn_loaded_cells.add(cell)

    stroke = Stroke(500, 500)
    strokes.add(stroke)


def game_board_clear():
    """ Чистит игровое поле: удаляет объекты, рисунки и клетки """
    for spr in all_sprites:
        spr.kill()


def process_move_consequences(rule_num, fig_pos):
    """ Обрабатывает actions: применяет фильтры после очередного хода
     rule_num - номер разрешающего правила (turns)
     fig_pos - координаты фигуры, тип event.pos"""
    l_s_source_name = "process_move_consequences"
    #print('rule', rule_num)
    if rule_num is not None:
        if 0 < rule_num < len(g_turns):
            # работаем с ним
            for l_cur_action in g_turns[rule_num][5]:  # перебираем actions текущего хода
                #print('action', l_cur_action)
                for l_cur_dir in l_cur_action[0]:  # перебираем направления текущего action
                    if l_cur_dir == 1:
                        dx = 1
                        dy = -1
                    elif l_cur_dir == 2:
                        dx = 1
                        dy = 0
                    elif l_cur_dir == 3:
                        dx = 1
                        dy = 1
                    elif l_cur_dir == 4:
                        dx = 0
                        dy = 1
                    elif l_cur_dir == 5:
                        dx = -1
                        dy = 1
                    elif l_cur_dir == 6:
                        dx = -1
                        dy = 0
                    elif l_cur_dir == 7:
                        dx = -1
                        dy = -1
                    elif l_cur_dir == 8:
                        dx = 0
                        dy = -1
                    else:
                        dx = 0
                        dy = 0
                    # проверим, не вылезаем ли мы по фильтру И целевому шаблону за пределы игрового поля
                    if (0 <= fig_pos[0] + (len(l_cur_action) - 2) * dx < g_CELLS_WIDTH) and \
                            (0 <= fig_pos[1] + (len(l_cur_action) - 2) * dy < g_CELLS_HEIGHT) and \
                         (0 <= fig_pos[0] + len(l_cur_action[-1]) * dx < g_CELLS_WIDTH) and \
                            (0 <= fig_pos[1] + len(l_cur_action[-1]) * dy < g_CELLS_HEIGHT):
                        l_pattern_fl = True
                        for i_loc in range(1, len(l_cur_action) - 1):
                            l_value_lgb = lst_game_board[fig_pos[1] + i_loc * dy][fig_pos[0] + i_loc * dx]
                            #print('0 in', 0 in l_cur_action[i_loc])
                            #print('lgb in', l_value_lgb in l_cur_action[i_loc])
                            if (0 in l_cur_action[i_loc]) or (l_value_lgb in l_cur_action[i_loc]):
                                l_pattern_fl = l_pattern_fl  # заглушка
                            else:
                                l_pattern_fl = False

                        # шаблон совпал с реальностью
                        #print('l_pattern_fl =', l_pattern_fl)
                        if l_pattern_fl:
                            for i_loc in range(1, len(l_cur_action[-1]) + 1):
                                #print('by i_loc', l_cur_action[-1][i_loc - 1])
                                #print('dir', l_cur_dir)
                                #print('lst_game_board', lst_game_board[fig_pos[1] + i_loc * dy][fig_pos[0] + i_loc * dx])
                                #print('l_cur_action', l_cur_action[-1])
                                if l_cur_action[-1][i_loc - 1] is None:
                                    i_loc = i_loc
                                elif l_cur_action[-1][i_loc - 1] == 0:
                                    # удаляем
                                    #for ggg in lst_game_board: print('before kill:', ggg)
                                    lst_game_board[fig_pos[1] + i_loc * dy][fig_pos[0] + i_loc * dx] = None
                                    #for ggg in lst_game_board: print('after new:', ggg)
                                    for fig in all_figures:
                                        if align_const(fig.rect.center) == (fig_pos[0] + i_loc * dx, fig_pos[1] + i_loc * dy):
                                            fig.kill()
                                else:
                                    #for ggg in lst_game_board: print('before kill:', ggg)
                                    lst_game_board[fig_pos[1] + i_loc * dy][fig_pos[0] + i_loc * dx] = l_cur_action[-1][i_loc - 1]
                                    #for ggg in lst_game_board: print('after new:', ggg)
                                    for fig in all_figures:
                                        if align_const(fig.rect.center) == (fig_pos[0] + i_loc * dx, fig_pos[1] + i_loc * dy):
                                            fig.kill()
                                    figure = Figure(fig_pos[0] + i_loc * dx, fig_pos[1] + i_loc * dy, l_cur_action[-1][i_loc - 1])
                                    all_figures.add(figure)
                                    all_sprites.add(figure)


        else:
            log_write(l_s_source_name, "caught incorrect value of turn: " + rule_num)
    else:
        log_write(l_s_source_name, "caught incorrect value of turn: " + rule_num)


def process_special_cells():
    global lst_game_board, g_special_cells_lst
    for l_list in g_special_cells_lst:  # l_list - одна запись
        #print(l_list)
        if lst_game_board[l_list[0][1]][l_list[0][0]] == l_list[0][2]:
            lst_game_board[l_list[0][1]][l_list[0][0]] = None
            for fig in all_figures:
                if align_const(fig.rect.center) == (l_list[0][0], l_list[0][1]):
                    fig.kill()
            lst_game_board[l_list[1][1]][l_list[1][0]] = l_list[1][2]
            figure = Figure(l_list[1][0], l_list[1][1], l_list[1][2])
            all_figures.add(figure)
            all_sprites.add(figure)


def make_points(figure):
    for j in range(len(lst_game_board)):
        for i in range(len(lst_game_board[j])):
            if is_turn_possible_f(figure, (i, j)) is not None:
                if g_turns[is_turn_possible_f(figure, (i, j))][6] == g_MAX_PRIORITY_TURN or \
                        figure.in_composite_turn and g_turns[is_turn_possible_f(figure, (i, j))][6] == max_priority_turn_f(figure):
                    Point(i, j)


def remove_points():
    """ Убирает с доски точки, отмечающие клетки для возможных ходов."""
    for pt in points:
        pt.kill()


def update_which_figures_can_move():
    for fig in all_figures:
        if fig.player_num == g_CURRENT_PLAYER:
            fig.can_move = True
        else:
            fig.can_move = False


# возможно, не понадобится
def is_there_a_max_priority_turn():
        return None


# открываем log
log_open("checkersplatform.log")

init_rules()


# Подготовка основного скрипта
pygame.init()
clock = pygame.time.Clock()
borders = pygame.sprite.Group()
all_figures = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
strokes = pygame.sprite.Group()
buttons = pygame.sprite.Group()
points = pygame.sprite.Group()
scrollers = pygame.sprite.Group()
drawn_two_color_cells = pygame.sprite.Group()
drawn_colored_cells = pygame.sprite.Group()
drawn_loaded_cells = pygame.sprite.Group()

manager = pygame_gui.UIManager((g_WIDTH, g_HEIGHT + 150))

game_board_loading()


whats_new_window = pygame.Surface((g_WIDTH * 0.5, g_HEIGHT * 0.75))
whats_new_window_rect = whats_new_window.get_rect()
term_text_surf = pygame.Surface((g_WIDTH * 0.5, g_HEIGHT))
term_text_surf.fill(NAVY)
term_text_surf.set_colorkey(NAVY)
whats_new_window_rect.center = g_WIDTH // 2, g_HEIGHT // 2
release_notes_bar = Scrollbar(20, 100)
release_notes_bar.rect.topright = whats_new_window_rect.topright
read_release_notes_file()


init_rules()

# Системные глобальные переменные
g_Logfile = ''
g_s_source_name = 'main'

## Здесь будет обрабатываться логотип
'''logo = pygame.image.load("logo.jpg")
pygame.transform.scale(logo, (g_WIDTH, g_HEIGHT))
logo_rect = logo.get_rect()
all_sprites.add(logo)
'''

l_source_fl = False
l_dest_fl = False
running = True
chosen_source_fig = None
num_of_losers = 0  # кол-во игроков, которые не смогли сделать ход
fl_check_possible_move = True


#if is_game_finished() != 0:
#    g_game_status = c_GAME_STATUS_FINISHED


num_of_losers = 0
while fl_check_possible_move:

        if num_of_losers == g_PLAYER_COUNT:
            # Всё. Игра окончена
            print_info("That's all. No one player can move. The game has been finished")
            g_game_status = c_GAME_STATUS_FINISHED
            fl_check_possible_move = False

        if not is_any_turns(g_CURRENT_PLAYER):
            #print(g_CURRENT_PLAYER, "- this player has no move")
            # передать ход
            g_CURRENT_PLAYER += 1
            if g_CURRENT_PLAYER > g_PLAYER_COUNT:
                g_CURRENT_PLAYER = 1

        else:
            fl_check_possible_move = False

        num_of_losers += 1

print_game_name(str(g_game_name))
print_player_count(str(g_PLAYER_COUNT))
print_player_move(str(g_CURRENT_PLAYER))
print_game_status("")
print_info("Ok, let's go!")

pygame.draw.line(interface_screen, BLACK, [90, 20], [90, 130], 4)

button_of_new = Button(10, 25, (70, 30), "button_new")
draw_text(button_of_new.image, "New", 30, BLACK, 0, -1)
#button_of_new.rect.center = 30, 30
buttons.add(button_of_new)

button_of_load = Button(10, 70, (70, 30), "button_load")
draw_text(button_of_load.image, "Load", 30, BLACK, 0, -1)
#button_of_load.rect.center = 30, 70
buttons.add(button_of_load)


button_of_release_notes = Button(10, 115, (70, 20), "button_release_notes")
draw_text(button_of_release_notes.image, "Updates", 18, BLACK, 0, -1)
#button_of_release_notes.rect.center = 30, 70
buttons.add(button_of_release_notes)


# Для отладки
#for ggg in lst_game_board: print(ggg)
#for ggg in g_figure_types: print(ggg)
#for ggg in g_turns: print(ggg)

g_modal_window = False

while running:

    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and not g_modal_window:
            if check_table_field(event) == 0:  # кликнули в игровое поле
                if g_game_status is c_GAME_STATUS_FINISHED:  # если игра завершена
                    g_game_status = g_game_status
                else:
                    ac = align_const(event.pos)
                    cell = lst_game_board[ac[1]][ac[0]]
                    if cell is not None:  # Если не None (т. е. если занятое поле)
                        cur_fig = find_figure_by_coors(align(event.pos))
                        if cur_fig.can_move:  # если эта фигура может ходить
                                    abs_max_priority_turn()
                                    remove_points()
                                    chosen_source_fig = cur_fig
                                    stroke.rect.center = cur_fig.rect.center
                                    l_source_fl = True
                                    source_coors = chosen_source_fig.rect.center  # координаты на доске
                                    l_dest_fl = False
                                    make_points(cur_fig)

                    else:  # Если   мы щёлкнули по чему-то, что не является нашей фигурой    пустое поле
                        l_dest_fl = True
                        dest_coors = align(event.pos)  # координаты на доске

                    if l_source_fl and l_dest_fl:  # выбраны и фигура, и поле для хода; проверяем, и, возможно, делаем ход
                        # преобразовать координаты в номера ячеек
                        source_pos_gbl = align_const(chosen_source_fig.rect.center)  # старые координаты фигуры
                        destination_pos_gbl = align_const(event.pos)  # новые координаты фигуры
                        # если такой ход этой фигурой допустим
                        l_turn_result = is_turn_possible_f(chosen_source_fig, destination_pos_gbl)
                        if l_turn_result is not None:
                            #print(chosen_source_fig.in_composite_turn, chosen_source_fig.can_move, l_turn_result, '',
                                  #g_turns[l_turn_result][6], g_MAX_PRIORITY_TURN, max_priority_turn_f(chosen_source_fig))
                            if g_turns[l_turn_result][6] == g_MAX_PRIORITY_TURN or \
                                    chosen_source_fig.in_composite_turn and g_turns[l_turn_result][6] == max_priority_turn_f(chosen_source_fig):
                                # занести запись о ходе в лог партии
                                g_history_of_a_game.append(g_turns[l_turn_result])
                                # убрать маркеры - обозначения ходов
                                remove_points()
                                # выполнить ход
                                chosen_source_fig.movement(event.pos)
                                # отработать последствия хода
                                process_move_consequences(l_turn_result, destination_pos_gbl)
                                # отработать ситуативные последствия (если есть)
                                process_special_cells()
                                #print("after sp_cells")
                                #for ggg in lst_game_board: print('g_brd', ggg)
                                # проверить, не закончена ли игра
                                winner_number = is_game_finished()
                                if winner_number != 0:
                                    g_game_status = c_GAME_STATUS_FINISHED
                                    print_info("The winner is player " + str(winner_number))
                                    print_game_status("Finished")
                                # снять выделение
                                stroke.rect.center = (-100, -100)
                                # сбросить флаги l_source_fl и l_dest_fl
                                l_source_fl = False
                                l_dest_fl = False
                                # передать ход
                                fl_check_possible_move = True
                                num_of_losers = 0
                                #g_CURRENT_PLAYER += 1
                                g_CURRENT_PLAYER = chosen_source_fig.player_num + 1
                                if g_CURRENT_PLAYER > g_PLAYER_COUNT:
                                    g_CURRENT_PLAYER = 1
                                update_which_figures_can_move()
                                for fig in all_figures:
                                    fig.in_composite_turn = False
                                if g_turns[l_turn_result][7]:
                                    chosen_source_fig.can_move = True
                                    chosen_source_fig.in_composite_turn = True
                                print_player_move(str(g_CURRENT_PLAYER))
                                if g_game_status != c_GAME_STATUS_FINISHED:
                                    while fl_check_possible_move:
                                        if num_of_losers == g_PLAYER_COUNT:
                                            # Всё. Игра окончена
                                            #print("That's all. No one player can move. The game has been finished")
                                            g_game_status = c_GAME_STATUS_FINISHED

                                        if not is_any_turns(g_CURRENT_PLAYER):
                                            #print(g_CURRENT_PLAYER, "- this player has no move")
                                            # передать ход
                                            g_CURRENT_PLAYER += 1
                                            if g_CURRENT_PLAYER > g_PLAYER_COUNT:
                                                g_CURRENT_PLAYER = 1
                                            print_player_move(str(g_CURRENT_PLAYER))

                                        else:
                                            fl_check_possible_move = False

                                        num_of_losers += 1
                                    chosen_source_fig = None


                            else:  # ход сделать нельзя
                                l_dest_fl = False
            else:  # если кликнули в интерфейс
                for butt in buttons:
                    if (butt.rect.x < event.pos[0] < butt.rect.bottomright[0]) and \
                            (butt.rect.y < event.pos[1] - g_HEIGHT < butt.rect.bottomright[1]):
                        butt.on_button_new_click()

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == g_file_selection.ok_button:
                        g_file_name_rules = str(g_file_selection.current_file_path).strip()
                        l_fl = load_game_rules(g_file_name_rules)
                        game_board_clear()
                        game_board_loading()
                        print_game_name(str(g_game_name))
                        print_game_status("")
                        print_player_count(str(g_PLAYER_COUNT))
                        print_player_move(str(g_CURRENT_PLAYER))
                        if l_fl:
                            print_info("Error during loading rules from " + str(g_file_name_rules) + ". Check log")
                        else:
                            print_info("Rules from " + g_file_name_rules + " loaded successfully")

                        #print(g_file_selection.current_file_path)
                        g_modal_window = False
            elif event.ui_element == g_file_selection.cancel_button:
                    #print("cancel_button")
                    g_modal_window = False
        elif event.type == pygame_gui.UI_WINDOW_CLOSE:
            #if event.ui_element == g_file_selection:
                    #print("close_button")
                    g_modal_window = False

        #if event.type == pygame.MOUSEBUTTONDOWN:

            #if g_file_selection is not None:
                #print(g_file_selection)
                #g_file_selection.groups
                #g_modal_window = False

        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

    # Обновление
    manager.update(time_delta)

    # Отрисовка
    screen.fill(g_GAME_BOARD_COLOUR)
    '''screen.blit(logo, logo_rect)'''
    borders.draw(screen)
    drawn_two_color_cells.draw(screen)
    drawn_colored_cells.draw(screen)
    drawn_loaded_cells.draw(screen)
    all_figures.draw(screen)
    points.draw(screen)
    strokes.draw(screen)
    screen.blit(interface_screen, (0, g_HEIGHT))
    buttons.draw(interface_screen)
    if g_showing_whats_new_fl:
        show_whats_new()
    manager.draw_ui(screen)
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()

log_close()

# Комметарии, которые мне ещё пригодятся
