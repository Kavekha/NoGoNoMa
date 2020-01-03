from bearlibterminal import terminal

import itertools

from ui_system.interface import Interface
from ui_system.render_functions import print_shadow
from ui_system.ui_enums import Layers


def draw_background(window_x, window_y, window_end_x, window_end_y):
    terminal.color('grey')
    terminal.layer(Layers.BACKGROUND_MENU.value)

    for x, y in itertools.product(range(window_x, window_end_x + 1), range(window_y, window_end_y + 1)):
        # coins
        if x == window_x and y == window_y:
            terminal.put(x, y, Interface.get_code('system/ui1.png'))
        elif x == window_end_x and y == window_y:
            terminal.put(x, y, Interface.get_code('system/ui3.png'))
        elif x == window_x and y == window_end_y:
            terminal.put(x, y, Interface.get_code('system/ui7.png'))
        elif x == window_end_x and y == window_end_y:
            terminal.put(x, y, Interface.get_code('system/ui9.png'))
        # bordures
        elif y == window_y:
            terminal.put(x, y, Interface.get_code('system/ui2.png'))
        elif x == window_x:
            terminal.put(x, y, Interface.get_code('system/ui4.png'))
        elif x == window_end_x:
            terminal.put(x, y, Interface.get_code('system/ui6.png'))
        elif y == window_end_y:
            terminal.put(x, y, Interface.get_code('system/ui8.png'))
        else:
            terminal.put(x, y, Interface.get_code('system/ui5.png'))


def draw_text(window_x, window_y, window_end_x, window_end_y, header, text):
    x_center = (window_end_x - window_x) // 2 + window_x
    y = window_y + 1
    header_center = x_center - (len(header) // 2)
    x = window_x + 2
    terminal.color('white')

    print_shadow(header_center, y, header)
    y += 2

    print_shadow(x, y, text)


def draw_tile_menu(window_x, window_y, window_end_x, window_end_y, header, text):
    terminal.layer(Layers.MENU.value)
    draw_background(window_x, window_y, window_end_x, window_end_y)
    draw_text(window_x, window_y, window_end_x, window_end_y, header, text)


def draw_ascii_menu(window_x, window_y, window_end_x, window_end_y, header, text):
    terminal.layer(Layers.MENU.value)
    draw_text(window_x, window_y, window_end_x, window_end_y, header, text)
