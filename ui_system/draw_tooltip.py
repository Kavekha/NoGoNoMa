from bearlibterminal import terminal

import config
from world import World
from ui_system.ui_enums import Layers
from components.position_component import PositionComponent
from components.name_component import NameComponent


def draw_tooltip():
    # mouse & tooltip
    terminal.layer(Layers.TOOLTIP.value)
    terminal.clear_area(0, 0, config.MAP_WIDTH, config.MAP_HEIGHT)

    subjects = World.get_components(PositionComponent, NameComponent)
    if not subjects:
        return

    mouse_pos_x = terminal.state(terminal.TK_MOUSE_X)
    mouse_pos_y = terminal.state(terminal.TK_MOUSE_Y)

    if mouse_pos_x < config.MAP_WIDTH or mouse_pos_y < config.MAP_HEIGHT:
        tooltip = []
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
            terminal.refresh()