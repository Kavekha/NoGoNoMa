from bearlibterminal import terminal

import re

from ui_system.interface import Interface
from texts import Texts


def print_shadow(x, y, text, shadow_offset=1):
    try:
        """Print text with shadow."""
        # remove color options for drawing shadow which has to be always black
        pattern = r'\[/?color.*?\]'
        no_color_text = re.sub(pattern, '', text)

        terminal.composition(terminal.TK_ON)

        # print shadow text
        terminal.printf(x, y, '[color=black][offset=0, {0}]{1}'.format(shadow_offset, no_color_text))
        terminal.printf(x, y, '[color=black][offset={0}, {0}]{1}'.format(shadow_offset, no_color_text))

        # print foreground text
        terminal.printf(x, y, text)

        terminal.composition(terminal.TK_OFF)
    except:
        print(f'print shadow error with : {text}')
        terminal.printf(x, y, text)


def render_bar(x, y, width, name, value, max_value, bar_color, back_color, text_color):
    value_bar = int(value / max_value * width)
    tile = Interface.get_code('system/ui5.png')

    # background bar
    terminal.color(back_color)
    for i in range(width):
        terminal.put(x + i, y, tile)

    # value bar
    if value_bar > 0:
        terminal.color(bar_color)
        for i in range(value_bar):
            terminal.put(x + i, y, tile)

    # text on it
    terminal.composition(terminal.TK_ON)
    text = f'{Texts.get_text(name)}: {value}/{max_value}'
    center_bar_x = x - (len(text) // 2) + (width // 2)
    terminal.color(text_color)
    print_shadow(center_bar_x, y, text)
    terminal.composition(terminal.TK_OFF)




