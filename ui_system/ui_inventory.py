from bearlibterminal import terminal

from world import World
from components.name_component import NameComponent
from components.in_backpack_component import InBackPackComponent
from ui_system.ui_enums import Layers, ItemMenuResult
from player_systems.player_input import inventory_input


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
    terminal.printf(18, y -2, f'[color=yellow] Inventory [/color]')

    letter_index = ord('a')
    for item in items_in_user_backpack:
        terminal.printf(17, y,
                        f'([color=orange]{chr(letter_index)}[/color])'
                        f' {World.get_entity_component(item, NameComponent).name}')
        y += 1
        letter_index += 1
    terminal.printf(18, y + 4, f'[color=darker yellow] ESCAPE to cancel.[/color]')

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
    terminal.printf(18, y - 2, f'[color=yellow] Drop which item?[/color]')

    letter_index = ord('a')
    for item in items_in_user_backpack:
        terminal.printf(17, y,
                        f'([color=orange]{chr(letter_index)}[/color])'
                        f' {World.get_entity_component(item, NameComponent).name}')
        y += 1
        letter_index += 1
    terminal.printf(18, y + 4, f'[color=darker yellow] ESCAPE to cancel.[/color]')

    terminal.refresh()

    return inventory_input(items_in_user_backpack)
