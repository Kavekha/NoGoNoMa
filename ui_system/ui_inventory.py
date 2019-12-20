'''
from bearlibterminal import terminal

from world import World
from components.name_component import NameComponent
from components.in_backpack_component import InBackPackComponent
from ui_system.ui_enums import Layers
from player_systems.player_input import inventory_input
from player_systems.game_system import get_item_color
from texts import Texts


def show_inventory(user):
    subjects = World.get_components(NameComponent, InBackPackComponent)
    if not subjects:
        return

    items_in_user_backpack = []
    for entity, (name, in_backpack, *args) in subjects:
        if in_backpack.owner == user:
            items_in_user_backpack.append(entity)

    terminal.layer(Layers.MENU.value)
    y = (25 - (len(items_in_user_backpack) //2))
    terminal.printf(18, y -2, f'[color=yellow] {Texts.get_text("INVENTORY")} [/color]')

    letter_index = ord('a')
    for item in items_in_user_backpack:
        terminal.printf(17, y,
                        f'([color=orange]{chr(letter_index)}[/color])'
                        f' [color={get_item_color(item)}]{World.get_entity_component(item, NameComponent).name}[/color]')
        y += 1
        letter_index += 1
    terminal.printf(18, y + 4, f'[color=darker yellow] {Texts.get_text("ESCAPE_TO_CANCEL")}[/color]')

    terminal.refresh()

    return inventory_input(items_in_user_backpack)


def drop_item_menu(user):
    subjects = World.get_components(NameComponent, InBackPackComponent)
    if not subjects:
        return

    items_in_user_backpack = []
    for entity, (name, in_backpack, *args) in subjects:
        if in_backpack.owner == user:
            items_in_user_backpack.append(entity)

    terminal.layer(Layers.MENU.value)
    y = (25 - (len(items_in_user_backpack) // 2))
    terminal.printf(18, y - 2, f'[color=yellow] {Texts.get_text("DROP_WHICH_ITEM")}[/color]')

    letter_index = ord('a')
    for item in items_in_user_backpack:
        terminal.printf(17, y,
                        f'([color=orange]{chr(letter_index)}[/color])'
                        f' [color={get_item_color(item)}]{World.get_entity_component(item, NameComponent).name}[/color]')
        y += 1
        letter_index += 1
    terminal.printf(18, y + 4, f'[color=darker yellow] ESCAPE to cancel.[/color]')

    terminal.refresh()

    return inventory_input(items_in_user_backpack)
    '''
