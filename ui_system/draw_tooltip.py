from bearlibterminal import terminal

from world import World
from ui_system.ui_enums import Layers
from ui_system.render_functions import get_item_display_name
from ui_system.render_camera import get_screen_bounds
from components.position_component import PositionComponent
from components.name_component import NameComponent
from components.hidden_component import HiddenComponent


def draw_tooltip():
    # render camera
    min_x, max_x, min_y, max_y = get_screen_bounds()

    # mouse & tooltip
    mouse_pos_x = terminal.state(terminal.TK_MOUSE_X) + min_x
    mouse_pos_y = terminal.state(terminal.TK_MOUSE_Y) + min_y

    current_map = World.fetch('current_map')
    subjects = World.get_components(PositionComponent, NameComponent)

    if mouse_pos_x > current_map.width - 1 or mouse_pos_y > current_map.height - 1:
        return

    if current_map.visible_tiles[current_map.xy_idx(mouse_pos_x, mouse_pos_y)]:
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
        terminal.clear_area(0, 0, current_map.width, current_map.height)

        if tooltip:
            terminal.color('white')
            width = 0
            for string in tooltip:
                if width < len(string):
                    width = len(string)
                width += 3

            if mouse_pos_x > 40:
                arrow_pos = (mouse_pos_x - 2 - min_x, mouse_pos_y - min_y)
                left_x = mouse_pos_x - width - min_x
                y = mouse_pos_y - min_y
                for string in tooltip:
                    terminal.printf(left_x, y, f'[bkcolor=gray]{string}[/color]')
                    padding = (width - len(string) - 1)
                    for i in range(0, padding):
                        terminal.printf(arrow_pos[0] - i, y, f'[bkcolor=gray] [/color]')
                    y += 1
                terminal.printf(arrow_pos[0], arrow_pos[1], f'[bkcolor=gray]->[/color]')
            else:
                arrow_pos = (mouse_pos_x + 1 - min_x, mouse_pos_y - min_y)
                left_x = mouse_pos_x + 3 - min_x
                y = mouse_pos_y - min_y
                for string in tooltip:
                    terminal.printf(left_x, y, f'[bkcolor=gray]{string}[/color]')
                    padding = width - len(string) - 1
                    for i in range(0, padding):
                        terminal.printf(arrow_pos[0] + i, y, f'[bkcolor=gray] [/color]')
                        y += 1
                terminal.printf(arrow_pos[0], arrow_pos[1], f'[bkcolor=gray]<-[/color]')
        World.insert('tooltip', (tooltip, mouse_pos_x, mouse_pos_y))
        terminal.refresh()
