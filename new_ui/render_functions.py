from bearlibterminal import terminal

import re


def print_shadow(x, y, text, shadow_offset=1):
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