from bearlibterminal import terminal

from ui_system.interface import GraphicalModes, Interface
from ui_system.render_menus import draw_tile_menu, draw_ascii_menu
from world import World
from ui_system.ui_enums import Layers
from ui_system.menu import InventoryMenu, CharacterMenu, MainMenu, GameOverMenu, VictoryMenu, MainOptionsMenu
import config
from texts import Texts


def show_item_screen():
    inventory_menu = InventoryMenu(Texts.get_text("INVENTORY"))
    inventory_menu.initialize()


def show_selected_item_screen(item):
    inventory_menu = InventoryMenu(Texts.get_text("INVENTORY"))
    inventory_menu.selected_item = item
    inventory_menu.initialize()


def show_character_menu():
    character_menu = CharacterMenu(Texts.get_text("CHARACTER_SHEET_HEADER"))
    character_menu.initialize()


def show_main_menu():
    terminal.clear()
    main_menu = MainMenu(Texts.get_text("GAME_TITLE"))
    main_menu.initialize()


def show_game_over_menu():
    terminal.clear()
    game_over_menu = GameOverMenu(Texts.get_text("GAME_OVER"))
    game_over_menu.initialize()


def show_victory_menu():
    terminal.clear()
    victory_menu = VictoryMenu(Texts.get_text("VICTORY"))
    victory_menu.initialize()


def show_main_options_menu():
    terminal.clear()
    main_options_menu = MainOptionsMenu(Texts.get_text("OPTIONS_MENU"))
    main_options_menu.initialize()
    """
    terminal.layer(Layers.MENU.value)

    window_x = config.SCREEN_WIDTH // 4  # 20
    window_y = config.SCREEN_HEIGHT // 4  # 10
    window_end_x = window_x * 3  # 60
    window_end_y = window_y * 3  # 40

    header = f'[color=yellow]{Texts.get_text("OPTIONS_MENU")}[/color]'

    letter_index = ord('a')
    text = f'[color=orange]({chr(letter_index)}) {Texts.get_text("CHANGE_LANGUAGE")}[/color]' + '\n'
    letter_index += 1
    text += f'[color=orange]({chr(letter_index)}) {Texts.get_text("CHANGE_GRAPHICS")}[/color]' + '\n'
    letter_index += 1
    text += f'[color=orange]({chr(letter_index)}) {Texts.get_text("BACK_TO_MAIN_MENU")}[/color]'

    if Interface.mode == GraphicalModes.TILES:
        draw_tile_menu(window_x, window_y, window_end_x, window_end_y, header, text)
    else:
        draw_ascii_menu(window_x, window_y, window_end_x, window_end_y, header, text)
    terminal.refresh()
    """