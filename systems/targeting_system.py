from bearlibterminal import terminal

from systems.inventory_system import use_item
from world import World
from components.targeting_component import TargetingComponent
from components.viewshed_component import ViewshedComponent
from components.position_components import PositionComponent
from ui_system.ui_enums import Layers
from ui_system.render_camera import get_screen_bounds, draw_tile, render_entities_camera
from map_builders.commons import distance_to
from player_systems.player_input import targeting_input
from ui_system.interface import Interface, GraphicalModes


def show_targeting():
    player = World.fetch('player')
    player_pos = World.get_entity_component(player, PositionComponent)
    min_x, max_x, min_y, max_y = get_screen_bounds()
    current_map = World.fetch('current_map')

    viewshed = World.get_entity_component(player, ViewshedComponent)
    targeter = World.get_entity_component(player, TargetingComponent)
    available_cells = list()
    x = 0
    y = 0

    for row in viewshed.visible_tiles:
        for tile in row:
            if tile and distance_to(player_pos.x, player_pos.y, x, y) < targeter.range:
                screen_x = x - min_x
                screen_y = y - min_y
                if 1 < screen_x < (max_x - min_x) - 1 and 1 < screen_y < (max_y - min_y):
                    if Interface.mode == GraphicalModes.TILES:
                        draw_tile(screen_x * Interface.zoom, screen_y * Interface.zoom, ' ', 'particules/grid.png', 'light blue', Layers.INTERFACE)
                    elif Interface.mode == GraphicalModes.ASCII:
                        draw_tile(screen_x * Interface.zoom, screen_y * Interface.zoom, ' ',
                                  'system/grid.png', 'light blue', Layers.BACKGROUND, 'light blue')
                    else:
                        print(f'Targeting system: {Interface.mode} not supported')
                        raise NotImplementedError
                    available_cells.append(current_map.xy_idx(x, y))
                    print(f'target: x,y : {x, y}. Mscreen : {screen_x, screen_y}, screenZoom: {screen_x * Interface.zoom, screen_y * Interface.zoom}')
            x += 1
        y += 1
        x = 0

    mouse_pos_x = (terminal.state(terminal.TK_MOUSE_X) // Interface.zoom) + min_x
    mouse_pos_y = (terminal.state(terminal.TK_MOUSE_Y) // Interface.zoom) + min_y
    print(f'mouse : {mouse_pos_x, mouse_pos_y}')
    valid_target = False
    for idx in available_cells:
        cell_x, cell_y = current_map.index_to_point2d(idx)
        if mouse_pos_x == cell_x and mouse_pos_y == cell_y:
            valid_target = True

    render_entities_camera()
    terminal.refresh()
    return targeting_input(targeter.item, (mouse_pos_x, mouse_pos_y), valid_target)


def select_target(item_id, target_position):
    use_item(item_id, target_position)
