from bearlibterminal import terminal

from enum import Enum

from new_ui.menus import draw_tile_menu, draw_ascii_menu
from ui_system.ui_enums import Layers
from world import World
from components.attributes_component import AttributesComponent
from components.pools_component import Pools
import config
from texts import Texts


class GraphicalModes(Enum):
    ASCII = 0
    TILES = 1


class CurrentUI(Enum):
    MAIN_MENU = 0
    CHARACTER_SHEET = 1


class Interface:
    path_to_code = {}
    current_code = 0xE000
    code_limit = 0xF8FF
    mode = None
    current_menu = None

    def __init__(self, mode=GraphicalModes.TILES):
        Interface.mode = mode

    @staticmethod
    def get_code(path):
        real_path = '/'.join([config.TILE_DIR, path])
        return Interface.path_to_code.get(real_path, Interface.get_new_code_for_path(path))

    @staticmethod
    def get_new_code_for_path(path):
        real_path = '/'.join([config.TILE_DIR, path])
        options = f'{Interface.current_code}:{real_path}'
        terminal.set(options)
        Interface.path_to_code.update({real_path: Interface.current_code})
        Interface.current_code += 1
        return Interface.current_code - 1

    @staticmethod
    def clear():
        Interface.current_menu = None

    @staticmethod
    def show_character_sheet():
        Interface.current_menu = CurrentUI.CHARACTER_SHEET

        terminal.layer(Layers.MENU.value)
        # we get player infos we want to display
        player = World.fetch('player')
        player_attributes = World.get_entity_component(player, AttributesComponent)
        player_pools = World.get_entity_component(player, Pools)

        window_x = config.SCREEN_WIDTH // 4  # 20
        window_y = config.SCREEN_HEIGHT // 4    # 10
        window_end_x = window_x * 3     # 60
        window_end_y = window_y * 3     # 40

        header = Texts.get_text('CHARACTER_SHEET_HEADER')

        text = Texts.get_text('CHARACTER_SHEET_CONTENT_LEVEL').format(player_pools.level) + '\n'
        text += Texts.get_text('CHARACTER_SHEET_CONTENT_XP').format(player_pools.xp, player_pools.level * 100) + '\n' +\
                '\n' + '\n'
        text += Texts.get_text('CHARACTER_SHEET_CONTENT_ATTRIBUTES') + '\n' + '\n'
        text += Texts.get_text('CHARACTER_SHEET_CONTENT_MIGHT').format(player_attributes.might) + '\n'
        text += Texts.get_text('CHARACTER_SHEET_CONTENT_BODY').format(player_attributes.body) + '\n'
        text += Texts.get_text('CHARACTER_SHEET_CONTENT_QUICKNESS').format(player_attributes.quickness) + '\n'
        text += Texts.get_text('CHARACTER_SHEET_CONTENT_WITS').format(player_attributes.wits)

        if Interface.mode == GraphicalModes.TILES:
            draw_tile_menu(window_x, window_y, window_end_x, window_end_y, header, text)
        else:
            draw_ascii_menu(window_x, window_y, window_end_x, window_end_y, header, text)
        terminal.refresh()


    @staticmethod
    def show_main_menu():
        Interface.current_menu = CurrentUI.MAIN_MENU

        terminal.layer(Layers.MENU.value)

        window_x = config.SCREEN_WIDTH // 4  # 20
        window_y = config.SCREEN_HEIGHT // 4    # 10
        window_end_x = window_x * 3     # 60
        window_end_y = window_y * 3     # 40

        header = f'[color=yellow]{Texts.get_text("GAME_TITLE")}[/color]'

        letter_index = ord('a')
        text = f'[color=orange]({chr(letter_index)}) {Texts.get_text("NEW_GAME")}[/color]' + '\n'
        letter_index += 1
        text += f'[color=orange]({chr(letter_index)}) {Texts.get_text("LOAD_GAME")}[/color]' + '\n'
        letter_index += 1
        text += f'[color=orange]({chr(letter_index)}) {Texts.get_text("CHANGE_LANGUAGE")}[/color]' + '\n'
        letter_index += 1
        text += f'[color=orange]({chr(letter_index)}) {Texts.get_text("QUIT")}[/color]'

        if Interface.mode == GraphicalModes.TILES:
            draw_tile_menu(window_x, window_y, window_end_x, window_end_y, header, text)
        else:
            draw_ascii_menu(window_x, window_y, window_end_x, window_end_y, header, text)
        terminal.refresh()
