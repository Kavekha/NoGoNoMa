from bearlibterminal import terminal

from ui_system.interface import GraphicalModes, Interface
from ui_system.render_menus import draw_tile_menu, draw_ascii_menu, draw_background
from ui_system.render_functions import get_item_color, get_item_display_name, print_shadow
from world import World
from components.attributes_component import AttributesComponent
from components.pools_component import Pools
from systems.inventory_system import get_equipped_items, get_items_in_inventory
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
    # header (Traduction, sans couleurs)
    # top: item selectionné
    # left: item list
    # right: description
    # bottom: options for selected item
    # end : how to quit
    terminal.layer(Layers.MENU.value)
    user = World.fetch('player')
    items_to_display = get_items_in_inventory(user)
    equipped = get_equipped_items(user)
    letter_index = ord('a')
    selected_item = None

    window_x = config.SCREEN_WIDTH // 8
    window_y = config.SCREEN_HEIGHT // 8
    window_end_x = window_x * 7
    total_width = (window_end_x - window_x)
    mutable_y = window_y
    mutable_y_right = window_y

    # header
    center_header_start = ((window_end_x - len(header)) // 2) #+ window_x
    header = f'[color=yellow] {header} [/color]'    # On ajoute la couleur après le len()
    print_shadow(center_header_start, mutable_y, header)
    mutable_y += 2
    mutable_y_right += 2

    # selected item
    if selected_item:
        selected_content = Texts.get_text(get_item_display_name(selected_item))
    else:
        selected_content = Texts.get_text('INVENTORY_USAGE_EXPLANATION')
    center_selected_item_start = ((window_end_x - len(selected_content)) // 2) # + window_x
    selected_content = f'[color=yellow] {selected_content} [/color]'
    print_shadow(center_selected_item_start, mutable_y, selected_content)
    mutable_y += 2
    mutable_y_right += 2

    # left: item list.
    item_list_max_width = total_width// 2    # Pour x 20, end 60 : 60 - 20 // 2 = 20
    for index, item in enumerate(items_to_display):
        chars_to_cut = 0
        # we need : letter_index + equipped_info + item_name
        item_name = Texts.get_text(get_item_display_name(item))
        if item in equipped:
            equipped_info = f'({Texts.get_text("EQUIPPED")})'
        else:
            equipped_info = ''
        final_msg = f'{chr(letter_index)}) {equipped_info} {item_name}'
        if len(final_msg) > item_list_max_width:
            chars_to_cut = item_list_max_width - len(final_msg)

        while chars_to_cut > 0:
            # on coupe d'abord equipped info:
            if len(equipped_info) > 3:
                equipped_info = {Texts.get_text("EQUIPPED")}[:1]
                equipped_info = f'({equipped_info})'
                final_msg = f'{chr(letter_index)}){equipped_info}{item_name}'
                if len(final_msg) > item_list_max_width:
                    chars_to_cut = item_list_max_width - len(final_msg)
            elif len(item_name) > 6:
                item_name = item_name[:6]
            else:
                # plus rien a faire possible.
                break
        # on ajoute la couleur de l'item
        final_msg = f'[color={get_item_color(item)}]({chr(letter_index)}) {equipped_info} {item_name}[/color]'
        print_shadow(window_x, mutable_y, final_msg)
        letter_index += 1
        mutable_y += 1

    # right: description
    if selected_item:
        from components.obfuscated_name_component import ObfuscatedNameComponent
        from components.consumable_component import ConsumableComponent
        from components.provides_healing_component import ProvidesHealingComponent
        from components.items_component import MeleeWeaponComponent

        # on recupere les infos.
        item_obfuscate = World.get_entity_component(selected_item, ObfuscatedNameComponent)
        item_consumable = World.get_entity_component(selected_item, ConsumableComponent)
        item_provide_healing = World.get_entity_component(selected_item, ProvidesHealingComponent)
        item_melee_weapon = World.get_entity_component(selected_item, MeleeWeaponComponent)

        item_description_width_total = (window_end_x - window_x) // 2
        item_description_width_start = window_x + item_list_max_width

        info_title = f'[color={config.COLOR_SYS_MSG}]{Texts.get_text("ITEM_INFO")}[/color]'
        print_shadow(item_description_width_start, mutable_y_right, info_title)
        mutable_y_right += 2

        if item_obfuscate:
            unknown_item_msg = Texts.get_text("CANT_KNOW_WITHOUT_USAGE_OR_IDENTIFICATION")
            full_text = list()
            while len(unknown_item_msg) > item_description_width_total:
                line = full_text[0: item_description_width_total - 2]
                full_text.append(line)
                unknown_item_msg = unknown_item_msg[item_description_width_total - 1:]
            if not full_text:
                full_text.append(unknown_item_msg)
            for line in full_text:
                print_shadow(item_description_width_start, mutable_y_right, line)
                mutable_y_right += 1
        else:
            if item_consumable:
                print_shadow(item_description_width_start, mutable_y_right, f'{Texts.get_text("ITEM_INFO_CONSUMMABLE")}')
                mutable_y_right += 1
            if item_provide_healing:
                print_shadow(item_description_width_start, mutable_y_right, f'{Texts.get_text("ITEM_INFO_HEALING")}')
                mutable_y_right += 1
            if item_melee_weapon:
                print_shadow(item_description_width_start, mutable_y_right, f'{Texts.get_text("ITEM_INFO_MELEE_WEAPON")}')
                mutable_y_right += 1

    # bottom: options if any.
    if selected_item:
        mutable_x = window_x
        available_options = [
            Texts.get_text('USE_ITEM'),
            Texts.get_text('DROP_ITEM'),
            Texts.get_text('EQUIP_ITEM'),
            Texts.get_text('UNEQUIP_ITEM')
        ]
        large_width = 0
        for option in available_options:
            if len(option) > large_width + 3:
                large_width = len(option)

        for option in available_options:
            print_shadow(mutable_x, mutable_y, option)
            mutable_x += large_width
            if mutable_x >= window_end_x:
                mutable_x = window_x
                mutable_y += 1
    mutable_y += 3

    # end : how to quit.
    exit_text = f' {Texts.get_text("ESCAPE_TO_CANCEL")} '
    center_exit_text_x = ((window_end_x - len(exit_text)) // 2) #+ window_x
    exit_text = f'[color=darker yellow]{exit_text}[/color]'
    print_shadow(center_exit_text_x, mutable_y, exit_text)
    mutable_y += 2

    if Interface.mode == GraphicalModes.TILES:
        draw_background(window_x, window_y, window_end_x, mutable_y)
    terminal.refresh()


def old_show_item_screen(header):
    user = World.fetch('player')
    items_to_display = get_items_in_inventory(user)
    equipped = get_equipped_items(user)
    letter_index = ord('a')

    window_x = config.SCREEN_WIDTH // 4  # 20
    window_y = config.SCREEN_HEIGHT // 6  # 10
    window_end_x = window_x * 3  # 60
    window_end_y = window_y * 5  # 40

    text = '\n'
    for index, item in enumerate(items_to_display):
        item_name = Texts.get_text(get_item_display_name(item))
        if item in equipped:
            equipped_info = f'({Texts.get_text("EQUIPPED")})'
        else:
            equipped_info = ''
        text += f'[color={get_item_color(item)}]({chr(letter_index)}) {equipped_info} {item_name}[/color]' + '\n'
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
