from bearlibterminal import terminal

from systems.system import System
from world import World
from components.combat_stats_component import CombatStatsComponent
from components.player_component import PlayerComponent
from components.name_component import NameComponent
from components.position_component import PositionComponent
from components.in_backpack_component import InBackPackComponent
from components.wants_to_drink_potion_component import WantToDrinkPotionComponent
from components.wants_to_drop_component import WantsToDropComponent
from data.types import ItemMenuResult
import config


class UiSystem(System):
    def __init__(self):
        self.line = config.UI_STATS

    def update(self, *args, **kwargs):
        # display HP
        subjects = World.get_components(CombatStatsComponent, PlayerComponent)
        if not subjects:
            return

        terminal.layer(0)
        for entity, (combat_stats, player) in subjects:
            terminal.printf(1, self.line, f'HP: {combat_stats.hp} / {combat_stats.max_hp}')

        #display logs
        log = World.fetch('logs')
        y = config.UI_LOG_FIRST_LINE
        for line in log:
            if y < config.SCREEN_HEIGHT:
                terminal.printf(2, y, line)
                y += 1


def draw_tooltip():
    # mouse & tooltip
    subjects = World.get_components(PositionComponent, NameComponent)
    if not subjects:
        return

    # Need terminal.read()
    mouse_pos_x = terminal.state(terminal.TK_MOUSE_X)
    mouse_pos_y = terminal.state(terminal.TK_MOUSE_Y)

    if mouse_pos_x < config.MAP_WIDTH or mouse_pos_y < config.MAP_HEIGHT:
        tooltip = []
        terminal.layer(0)
        for entity, (position, name) in subjects:
            if position.x == mouse_pos_x and position.y == mouse_pos_y:
                tooltip.append(f'{name.name}')

        if tooltip:
            width = 0
            for string in tooltip:
                if width < len(string):
                    width = len(string)
                width += 3

            if mouse_pos_x > 40:
                arrow_pos = (mouse_pos_x -2, mouse_pos_y)
                left_x = mouse_pos_x - width
                y = mouse_pos_y
                for string in tooltip:
                    terminal.printf(left_x, y, f'[bkcolor=gray]{string}[/color]')
                    padding = (width - len(string) - 1)
                    for i in range(0, padding):
                        terminal.printf(arrow_pos[0] -1, y, f'[bkcolor=gray] [/color]')
                    y += 1
                terminal.printf(arrow_pos[0], arrow_pos[1], f'[bkcolor=gray] -> [/color]')
            else:
                arrow_pos = (mouse_pos_x + 1, mouse_pos_y)
                left_x = mouse_pos_x +3
                y = mouse_pos_y
                for string in tooltip:
                    terminal.printf(left_x, y, f'[bkcolor=gray]{string}[/color]')
                    padding = width - len(string) - 1
                    for i in range(0, padding):
                        terminal.printf(arrow_pos[0] - 1, y, f'[bkcolor=gray] [/color]')
                        y += 1
                terminal.printf(arrow_pos[0], arrow_pos[1], f'[bkcolor=gray] <- [/color]')


def show_inventory(user):
    subjects = World.get_components(NameComponent, InBackPackComponent)
    if not subjects:
        return

    items_in_user_backpack = []
    for entity, (name, in_backpack, *args) in subjects:
        if in_backpack.owner == user:
            items_in_user_backpack.append(entity)

    previous_layer = terminal.state(terminal.TK_LAYER)
    terminal.layer(3)

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
    terminal.layer(previous_layer)

    if terminal.has_input():
        key = terminal.read()
        if key == terminal.TK_ESCAPE:
            return ItemMenuResult.CANCEL, None
        else:
            index = terminal.state(terminal.TK_CHAR) - ord('a')
            if 0 <= index < len(items_in_user_backpack):
                return ItemMenuResult.SELECTED, items_in_user_backpack[index]
            return ItemMenuResult.NO_RESPONSE, None
    return ItemMenuResult.NO_RESPONSE, None


def select_item_from_inventory(item_id):
    drink_intent = WantToDrinkPotionComponent(item_id)
    player = World.fetch('player')
    World.add_component(drink_intent, player)


def drop_item_from_inventory(item_id):
    drop_intent = WantsToDropComponent(item_id)
    player = World.fetch('player')
    World.add_component(drop_intent, player)


def drop_item_menu(user):
    subjects = World.get_components(NameComponent, InBackPackComponent)
    if not subjects:
        return

    items_in_user_backpack = []
    for entity, (name, in_backpack, *args) in subjects:
        if in_backpack.owner == user:
            items_in_user_backpack.append(entity)

    previous_layer = terminal.state(terminal.TK_LAYER)
    terminal.layer(3)

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
    terminal.layer(previous_layer)

    if terminal.has_input():
        key = terminal.read()
        if key == terminal.TK_ESCAPE:
            return ItemMenuResult.CANCEL, None
        else:
            index = terminal.state(terminal.TK_CHAR) - ord('a')
            if 0 <= index < len(items_in_user_backpack):
                return ItemMenuResult.SELECTED, items_in_user_backpack[index]
            return ItemMenuResult.NO_RESPONSE, None
    return ItemMenuResult.NO_RESPONSE, None
