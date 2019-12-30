from bearlibterminal import terminal
from world import World
from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent
from components.hidden_component import HiddenComponent
from ui_system.interface import Interface, GraphicalModes
from ui_system.ui_enums import Layers
from gmap.gmap_enums import TileType
import config


def get_screen_bounds():
    player = World.fetch('player')
    player_pos = World.get_entity_component(player, PositionComponent)

    center_x = config.SCREEN_WIDTH // 2
    center_y = config.SCREEN_HEIGHT // 2
    min_x = player_pos.x - center_x
    max_x = min_x + config.SCREEN_WIDTH
    min_y = player_pos.y - center_y
    max_y = min_y + config.SCREEN_HEIGHT

    return min_x, max_x, min_y, max_y


def render_map_camera():
    current_map = World.fetch('current_map')
    min_x, max_x, min_y, max_y = get_screen_bounds()
    map_width = current_map.width
    map_height = current_map.height

    y = 0
    for ty in range(min_y, max_y):
        x = 0
        for tx in range(min_x, max_x):
            if 0 < tx < map_width and 0 < ty < map_height:
                # terminal.layer(Layers.MAP.value)
                terminal.composition(terminal.TK_ON)
                idx = current_map.xy_idx(tx, ty)
                if current_map.revealed_tiles[idx]:
                    glyph, sprite, char_color = get_tile_glyph(idx, current_map)
                    draw_tile(x, y, glyph, sprite, char_color, Layers.MAP)

                    if current_map.stains[idx]:
                        # terminal.layer(Layers.STAINS.value)
                        char_color = 'dark red'
                        sprite = f'props/blood{current_map.stains[idx]}.png'
                        glyph = ' '
                        draw_tile(x, y, glyph, sprite, char_color, Layers.STAINS)
                elif config.SHOW_BOUNDARIES:
                    if Interface.mode == GraphicalModes.ASCII or Interface.mode == GraphicalModes.TILES:
                        terminal.printf(x, y, f'[color=gray]-[/color]')
                    else:
                        print(f'render camera: graphical mode {Interface.mode} not implemented.')
                        raise NotImplementedError
                terminal.composition(terminal.TK_OFF)
            x += 1
        y += 1


def render_entities_camera():
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
            entity_screen_x = position.x - min_x
            entity_screen_y = position.y - min_y
            if 0 < entity_screen_x < map_width and 0 < entity_screen_y < map_height:
                if Interface.mode == GraphicalModes.ASCII:
                    terminal.printf(entity_screen_x,
                                    entity_screen_y,
                                    f'[color={renderable.char_color}]{renderable.glyph}[/color]')
                elif Interface.mode == GraphicalModes.TILES:
                    terminal.color(f'{renderable.fg}')
                    terminal.put(entity_screen_x, entity_screen_y, Interface.get_code(renderable.sprite))
                else:
                    print(f'render camera: graphical mode {Interface.mode} not implemented.')
                    raise NotImplementedError


def draw_tile(x, y, glyph, sprite, char_color, render_order=None):
    if render_order:
        terminal.layer(render_order.value)
    if Interface.mode == GraphicalModes.ASCII:
        terminal.printf(x, y, f'[color={char_color}]{glyph}[/color]')
    elif Interface.mode == GraphicalModes.TILES:
        terminal.color(f'{char_color}')
        terminal.put(x, y, Interface.get_code(sprite))
    else:
        print(f'render camera: graphical mode {Interface.mode} not implemented.')
        raise NotImplementedError


def get_tile_glyph(idx, gmap):
    glyph = None
    char_color = None
    sprite = None

    if gmap.tiles[idx] == TileType.FLOOR:
        glyph = '.'
        char_color = 'dark yellow'
        sprite = 'map/ground.png'
    elif gmap.tiles[idx] == TileType.WALL:
        glyph = '#'
        char_color = 'darker yellow'
        sprite = 'map/wall1.png'
    elif gmap.tiles[idx] == TileType.DOWN_STAIRS:
        glyph = '>'
        char_color = 'lighter blue'
        sprite = 'map/stairs_down.png'
    elif gmap.tiles[idx] == TileType.EXIT_PORTAL:
        glyph = 'O'
        char_color = 'lighter cyan'
        sprite = 'map/stairs_down.png'

    if not gmap.visible_tiles[idx]:
        char_color = 'dark gray'

    return glyph, sprite, char_color
