from bearlibterminal import terminal

import config
from world import World
from gmap.utils import xy_idx
from ui_system.ui_enums import Layers
from ui_system.render_functions import get_item_display_name
from components.position_component import PositionComponent
from components.name_component import NameComponent
from components.hidden_component import HiddenComponent


def draw_tooltip():
    # mouse & tooltip
    mouse_pos_x = terminal.state(terminal.TK_MOUSE_X)
    mouse_pos_y = terminal.state(terminal.TK_MOUSE_Y)
    current_map = World.fetch('current_map')
    subjects = World.get_components(PositionComponent, NameComponent)

    if mouse_pos_x > config.MAP_WIDTH - 1 or mouse_pos_y > config.MAP_HEIGHT - 1:
        return

    # current_map.revealed_tiles[xy_idx(mouse_pos_x, mouse_pos_y)] (Pour les revealed. Mais on voit pas les items)
    if current_map.visible_tiles[xy_idx(mouse_pos_x, mouse_pos_y)]:
        old_tooltip, old_mouse_x, old_mouse_y = World.fetch('tooltip')

        tooltip = []
        for entity, (position, name) in subjects:
            if World.get_entity_component(entity, HiddenComponent):
                continue
            if position.x == mouse_pos_x and position.y == mouse_pos_y:
                tooltip.append(get_item_display_name(entity))

        # identique, on ne change rien.
        if tooltip == old_tooltip and mouse_pos_x == old_mouse_x and mouse_pos_y == old_mouse_y:
            return

        terminal.layer(Layers.TOOLTIP.value)
        terminal.clear_area(0, 0, config.MAP_WIDTH, config.MAP_HEIGHT)

        # plus de tooltip a afficher
        if tooltip:
            terminal.color('white')
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
                terminal.printf(arrow_pos[0], arrow_pos[1], f'[bkcolor=gray]->[/color]')
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
                terminal.printf(arrow_pos[0], arrow_pos[1], f'[bkcolor=gray]<-[/color]')
        World.insert('tooltip', (tooltip, mouse_pos_x, mouse_pos_y))
        terminal.refresh()
