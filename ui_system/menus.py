from bearlibterminal import terminal

from ui_system.interface import GraphicalModes, Interface
from ui_system.render_menus import draw_tile_menu, draw_ascii_menu
from ui_system.render_functions import get_item_color, get_item_display_name
from world import World
from components.attributes_component import AttributesComponent
from components.pools_component import Pools
from systems.inventory_system import get_items_in_user_backpack
from ui_system.ui_enums import Layers
from player_systems.game_system import xp_for_next_level
import config
from texts import Texts


def show_character_sheet():
    terminal.layer(Layers.MENU.value)
    # we get player infos we want to display
    player = World.fetch('player')
    player_attributes = World.get_entity_component(player, AttributesComponent)
    player_pools = World.get_entity_component(player, Pools)

    window_x = config.SCREEN_WIDTH // 4  # 20
    window_y = config.SCREEN_HEIGHT // 4  # 10
    window_end_x = window_x * 3  # 60
    window_end_y = window_y * 3  # 40

    header = Texts.get_text('CHARACTER_SHEET_HEADER')

    text = Texts.get_text('CHARACTER_SHEET_CONTENT_LEVEL').format(player_pools.level) + '\n'
    text += Texts.get_text('CHARACTER_SHEET_CONTENT_XP').format(player_pools.xp,
                                                                xp_for_next_level(player_pools.level)) + '\n' + \
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


def show_main_menu():
    terminal.layer(Layers.MENU.value)

    window_x = config.SCREEN_WIDTH // 4  # 20
    window_y = config.SCREEN_HEIGHT // 4  # 10
    window_end_x = window_x * 3  # 60
    window_end_y = window_y * 3  # 40

    header = f'[color=yellow]{Texts.get_text("GAME_TITLE")}[/color]'

    letter_index = ord('a')
    text = f'[color=orange]({chr(letter_index)}) {Texts.get_text("NEW_GAME")}[/color]' + '\n'
    letter_index += 1
    text += f'[color=orange]({chr(letter_index)}) {Texts.get_text("LOAD_GAME")}[/color]' + '\n'
    letter_index += 1
    text += f'[color=orange]({chr(letter_index)}) {Texts.get_text("OPTIONS_MENU")}[/color]' + '\n'
    letter_index += 1
    text += f'[color=orange]({chr(letter_index)}) {Texts.get_text("QUIT")}[/color]'

    if Interface.mode == GraphicalModes.TILES:
        draw_tile_menu(window_x, window_y, window_end_x, window_end_y, header, text)
    else:
        draw_ascii_menu(window_x, window_y, window_end_x, window_end_y, header, text)
    terminal.refresh()


def show_game_over_screen():
    window_x = config.SCREEN_WIDTH // 4  # 20
    window_y = config.SCREEN_HEIGHT // 4  # 10
    window_end_x = window_x * 3  # 60
    window_end_y = window_y * 3  # 40

    header = f'{Texts.get_text("GAME_OVER")}'
    text = '\n' + '\n'
    logs = World.fetch('logs')
    count = 0
    for log in logs:
        if count < 10:
            text += log + '\n'
            count += 1
        else:
            break
    text += '\n' + '\n'
    text += f'{Texts.get_text("PRESS_ESCAPE_TO_MAIN_MENU")}'

    if Interface.mode == GraphicalModes.TILES:
        draw_tile_menu(window_x, window_y, window_end_x, window_end_y, header, text)
    else:
        draw_ascii_menu(window_x, window_y, window_end_x, window_end_y, header, text)
    terminal.refresh()


def show_victory_screen():
    window_x = config.SCREEN_WIDTH // 4  # 20
    window_y = config.SCREEN_HEIGHT // 4  # 10
    window_end_x = window_x * 3  # 60
    window_end_y = window_y * 3  # 40

    header = f'{Texts.get_text("VICTORY")}'
    text = '\n'
    text += f'{Texts.get_text("YOU_ESCAPE_DUNGEON")}' + '\n'
    text += f'{Texts.get_text("PRESS_ESCAPE_TO_MAIN_MENU")}'

    if Interface.mode == GraphicalModes.TILES:
        draw_tile_menu(window_x, window_y, window_end_x, window_end_y, header, text)
    else:
        draw_ascii_menu(window_x, window_y, window_end_x, window_end_y, header, text)
    terminal.refresh()


def show_item_screen(header):
    window_x = config.SCREEN_WIDTH // 4  # 20
    window_y = config.SCREEN_HEIGHT // 4  # 10
    window_end_x = window_x * 3  # 60
    window_end_y = window_y * 3  # 40

    user = World.fetch('player')
    items_to_display = get_items_in_user_backpack(user)
    letter_index = ord('a')

    text = '\n'
    for index, item in enumerate(items_to_display):
        item_name = get_item_display_name(item)
        text += f'[color={get_item_color(item)}]({chr(letter_index)}) {Texts.get_text(item_name)}[/color]' + '\n'
        letter_index += 1

    text += '\n'
    text += f'[color=darker yellow] {Texts.get_text("ESCAPE_TO_CANCEL")}'

    if Interface.mode == GraphicalModes.TILES:
        draw_tile_menu(window_x, window_y, window_end_x, window_end_y, header, text)
    else:
        draw_ascii_menu(window_x, window_y, window_end_x, window_end_y, header, text)
    terminal.refresh()


def show_option_menu():
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

