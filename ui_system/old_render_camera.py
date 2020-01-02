from bearlibterminal import terminal

import time

from world import World
from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent
from components.hidden_component import HiddenComponent
from ui_system.interface import Interface, GraphicalModes
from ui_system.ui_enums import Layers
from ui_system.draw_tiles import draw_tile, get_tile_glyph
import config


def get_screen_bounds():
    player = World.fetch('player')
    player_pos = World.get_entity_component(player, PositionComponent)

    center_x = Interface.map_screen_width // 2
    center_y = Interface.map_screen_height // 2
    min_x = player_pos.x - center_x
    max_x = min_x + Interface.map_screen_width
    min_y = player_pos.y - center_y
    max_y = min_y + Interface.map_screen_height

    return min_x, max_x, min_y, max_y


def render_map_camera():
    start = time.perf_counter()

    current_map = World.fetch('current_map')
    min_x, max_x, min_y, max_y = get_screen_bounds()
    map_width = current_map.width
    map_height = current_map.height

    y = 0
    for ty in range(min_y, max_y):
        x = 0
        for tx in range(min_x, max_x):
            if 0 <= tx < map_width and 0 <= ty < map_height:
                terminal.composition(terminal.TK_ON)
                idx = current_map.xy_idx(tx, ty)
                if current_map.revealed_tiles[idx]:
                    glyph, sprite, char_color = get_tile_glyph(idx, current_map)
                    draw_tile(x, y, glyph, sprite, char_color, Layers.MAP)

                if current_map.stains[idx] and current_map.visible_tiles[idx]:
                    char_color = 'dark red'
                    sprite = f'props/blood{current_map.stains[idx]}.png'
                    glyph = ' '
                    draw_tile(x, y, glyph, sprite, char_color, Layers.STAINS)

                if config.SHOW_BOUNDARIES and not current_map.revealed_tiles[idx]:
                    if Interface.mode == GraphicalModes.ASCII or Interface.mode == GraphicalModes.TILES:
                        terminal.printf(x, y, f'[color=gray]-[/color]')
                    else:
                        print(f'render camera: graphical mode {Interface.mode} not implemented.')
                        raise NotImplementedError

                terminal.composition(terminal.TK_OFF)
            x += (1 * Interface.zoom)
        y += (1 * Interface.zoom)

    delta_time = (time.perf_counter() - start) * 1000
    print(f'delta time: for render map : {delta_time}')


def render_entities_camera():
    start = time.perf_counter()

    current_map = World.fetch('current_map')
    min_x, max_x, min_y, max_y = get_screen_bounds()
    map_width = current_map.width
    map_height = current_map.height

    subjects = World.get_components(PositionComponent, RenderableComponent)
    for entity, (position, renderable) in subjects:
        hidden = World.get_entity_component(entity, HiddenComponent)
        idx = current_map.xy_idx(position.x, position.y)
        terminal.layer(renderable.render_order.value)
        if current_map.visible_tiles[idx] and not hidden:
            entity_screen_x = ((position.x - min_x) * Interface.zoom)
            entity_screen_y = ((position.y - min_y) * Interface.zoom)
            if 0 <= entity_screen_x <= map_width and 0 <= entity_screen_y <= map_height:
                if Interface.mode == GraphicalModes.ASCII:
                    terminal.printf(entity_screen_x,
                                    entity_screen_y,
                                    f'[color={renderable.fg}]{renderable.glyph}[/color]')
                elif Interface.mode == GraphicalModes.TILES:
                    terminal.color(f'{renderable.fg}')
                    terminal.put(entity_screen_x, entity_screen_y, Interface.get_code(renderable.sprite))
                else:
                    print(f'render camera: graphical mode {Interface.mode} not implemented.')
                    raise NotImplementedError

    delta_time = (time.perf_counter() - start) * 1000
    print(f'delta time: for render entities : {delta_time}')


def render_debug_map(gmap):
    player = World.fetch('player')
    player_pos = World.get_entity_component(player, PositionComponent)

    center_x = Interface.map_screen_width // 2
    center_y = Interface.map_screen_height // 2
    player_pos.x = center_x
    player_pos.y = center_y

    min_x, max_x, min_y, max_y = get_screen_bounds()

    map_width = gmap.width - 1
    map_height = gmap.height - 1

    y = 0
    for ty in range(min_y, max_y):
        x = 0
        for tx in range(min_x, max_x):
            if 0 <= tx <= map_width and 0 <= ty <= map_height:
                idx = gmap.xy_idx(tx, ty)
                if gmap.revealed_tiles[idx]:
                    glyph, sprite, char_color = get_tile_glyph(idx, gmap)
                    draw_tile(tx, ty, glyph, sprite, char_color, render_order=Layers.MAP)
            elif config.SHOW_BOUNDARIES:
                if Interface.mode == GraphicalModes.ASCII or Interface.mode == GraphicalModes.TILES:
                    terminal.printf(x, y, f'[color=gray]-[/color]')
                else:
                    print(f'render camera: graphical mode {Interface.mode} not implemented.')
                    raise NotImplementedError
            x += (1 * Interface.zoom)
        y += (1 * Interface.zoom)

    draw_tile(0, 0, 'X', 'map/wall1.png', 'pink', render_order=Layers.MAP)
    draw_tile(gmap.width - 1, 0, 'X', 'map/wall1.png', 'pink', render_order=Layers.MAP)
    draw_tile(0, gmap.height - 1, 'X', 'map/wall1.png', 'pink', render_order=Layers.MAP)
    draw_tile(gmap.width - 1, gmap.height - 1, 'X', 'map/wall1.png', 'pink', render_order=Layers.MAP)

    terminal.refresh()
