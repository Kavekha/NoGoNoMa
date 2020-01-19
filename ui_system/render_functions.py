from bearlibterminal import terminal

import re

from ui_system.interface import Interface

from components.magic_item_components import MagicItemComponent
from components.name_components import NameComponent, ObfuscatedNameComponent
from components.item_components import ItemComponent
from components.item_components import ConsumableComponent

from data.components_enum import MagicItemClass
from texts import Texts
from world import World
import config


def print_shadow(x, y, text, shadow_offset=1):
    print(f'print shadow: {x, y, text, shadow_offset}')
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
    except Exception as e:
        print(f'print shadow error with : {text}')
        print(f'exception was: {e}')
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


def get_item_color(item_entity):
    magic_component = World.get_entity_component(item_entity, MagicItemComponent)
    result = config.COLOR_MAGIC_ITEM_COMMON
    if magic_component:
        if magic_component.magic_class == MagicItemClass.UNCOMMON:
            result = config.COLOR_MAGIC_ITEM_UNCOMMON
        if magic_component.magic_class == MagicItemClass.RARE:
            result = config.COLOR_MAGIC_ITEM_RARE
        elif magic_component.magic_class == MagicItemClass.EPIC:
            result = config.COLOR_MAGIC_ITEM_EPIC
        elif magic_component.magic_class == MagicItemClass.LEGENDARY:
            result = config.COLOR_MAGIC_ITEM_LEGENDARY

        if magic_component.cursed:
            item_named = World.get_entity_component(item_entity, NameComponent)
            master_dungeon = World.fetch('master_dungeon')
            # a été identifié?
            if item_named.name in master_dungeon.identified_items:
                result = config.COLOR_MAGIC_ITEM_CURSED

    return result


def get_item_display_name(item_id):
    master_dungeon = World.fetch('master_dungeon')
    item_name_comp = World.get_entity_component(item_id, NameComponent)

    if item_name_comp.name in master_dungeon.identified_items:
        item_consumable = World.get_entity_component(item_id, ConsumableComponent)
        if item_consumable:
            if item_consumable.charges > 1:
                # may crash if return to function that act on string.
                return f'{item_name_comp.name} - {item_consumable.charges} {Texts.get_text("CHARGES")}'
            return item_name_comp.name
    else:
        obfuscate_comp = World.get_entity_component(item_id, ObfuscatedNameComponent)
        if obfuscate_comp:
            return obfuscate_comp.name
        else:
            if World.get_entity_component(item_id, ItemComponent):
                return Texts.get_text('UNIDENTIFIED_ITEM')

    return Texts.get_text("UNKNOWN")


def get_obfuscate_name(item_id):
    name_c = World.get_entity_component(item_id, NameComponent)
    magic_c = World.get_entity_component(item_id, MagicItemComponent)

    if name_c:
        if magic_c:
            identified_items = World.fetch('master_dungeon').identified_items
            obfuscate_c = World.get_entity_component(item_id, ObfuscatedNameComponent)
            if name_c.name in identified_items:
                return name_c.name
            elif obfuscate_c:
                return obfuscate_c.name
            else:
                return Texts.get_text('UNIDENTIFIED_ITEM')
        else:
            return name_c.name
    else:
        print(f'get_obfuscate_name : nameless object send : entity {item_id}.')
        raise NotImplementedError
