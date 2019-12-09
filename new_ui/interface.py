from bearlibterminal import terminal
import re

from enum import Enum
import itertools
import os

from systems.system import System
from ui_system.ui_enums import Layers
import config


class GraphicalModes(Enum):
    ASCII = 0
    TILES = 1


SYSTEM = [
    'system/square.png',
    'system/base.png',
    'system/ui1.png',
    'system/ui2.png',
    'system/ui3.png',
    'system/ui4.png',
    'system/ui5.png',
    'system/ui6.png',
    'system/ui7.png',
    'system/ui8.png',
    'system/ui9.png'
]

TILE_DIR = 'tileset'


class Interface(System):
    def __init__(self, mode=GraphicalModes.TILES):
        self.mode = mode
        self.path_to_code = {}
        self.current_code = 0xE000
        self.code_limit = 0xF8FF

        for path in SYSTEM:
            real_path = '/'.join([TILE_DIR, path])
            options = f'{self.current_code}:{real_path}'
            terminal.set(options)
            self.path_to_code.update({real_path:self.current_code})
            self.current_code += 1

    def get_code(self, path):
        real_path = '/'.join([TILE_DIR, path])
        return self.path_to_code.get(real_path)

    def update(self):
        if terminal.peek() == terminal.TK_C:
            self.show_character_sheet()

    def draw_background(self, window_x, window_y, window_end_x, window_end_y):
        terminal.color('gray')

        for x, y in itertools.product(range(window_x, window_end_x + 1), range(window_y, window_end_y + 1)):
            # coins
            if x == window_x and y == window_y:
                terminal.put(x, y, self.get_code('system/ui1.png'))
            elif x == window_end_x and y == window_y:
                terminal.put(x, y, self.get_code('system/ui3.png'))
            elif x == window_x and y == window_end_y:
                terminal.put(x, y, self.get_code('system/ui7.png'))
            elif x == window_end_x and y == window_end_y:
                terminal.put(x, y, self.get_code('system/ui9.png'))
            # bordures
            elif y == window_y:
                terminal.put(x, y, self.get_code('system/ui2.png'))
            elif x == window_x:
                terminal.put(x, y, self.get_code('system/ui4.png'))
            elif x == window_end_x:
                terminal.put(x, y, self.get_code('system/ui6.png'))
            elif y == window_end_y:
                terminal.put(x, y, self.get_code('system/ui8.png'))
            else:
                terminal.put(x, y, self.get_code('system/ui5.png'))

    def draw_text(self, window_x, window_y, window_end_x, window_end_y, header, text):
        x_center = (window_end_x - window_x) // 2 + window_x
        y = window_y + 1
        header_center = x_center - (len(header) //2)
        x = window_x + 2
        terminal.color('white')

        print_shadow(header_center, y, header)
        y += 2

        for string in text:
            y += 1
            print_shadow(x, y, string)

    def draw_tile_menu(self, window_x, window_y, window_end_x, window_end_y, header, text):
        terminal.layer(Layers.MENU.value)
        self.draw_background(window_x, window_y, window_end_x, window_end_y)
        self.draw_text(window_x, window_y, window_end_x, window_end_y, header, text)
        terminal.refresh()

    def show_character_sheet(self):
        from world import World
        from components.attributes_component import AttributesComponent
        from components.pools_component import Pools

        # we get player infos we want to display
        player = World.fetch('player')
        player_attributes = World.get_entity_component(player, AttributesComponent)
        player_pools = World.get_entity_component(player, Pools)

        window_x = 20
        window_y = 10
        window_end_x = 60
        window_end_y = 40

        header = '-character sheet-'

        text = list()
        text.append(f'Level : {player_pools.level}')
        text.append(f'xp : {player_pools.xp} / {player_pools.level * 100}')
        text.append('')
        text.append('')
        text.append('* Attributes *')
        text.append('')
        text.append(f'Might : {player_attributes.might}')
        text.append(f'Body : {player_attributes.body}')
        text.append(f'Quickness : {player_attributes.quickness}')
        text.append(f'Wits : {player_attributes.wits}')

        if self.mode == GraphicalModes.TILES:
            self.draw_tile_menu(window_x, window_y, window_end_x, window_end_y, header, text)
        else:
            self.draw_ascii_menu(window_x, window_y, window_end_x, window_end_y, header, text)

        while True:
            if terminal.has_input():
                if terminal.read() == terminal.TK_ESCAPE:
                    terminal.clear_area(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
                    terminal.refresh()
                    break

    def draw_ascii_menu(self, window_x, window_y, window_end_x, window_end_y, header, text):
        terminal.layer(Layers.MENU.value)
        self.draw_text(window_x, window_y, window_end_x, window_end_y, header, text)
        terminal.refresh()


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
