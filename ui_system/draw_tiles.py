from bearlibterminal import terminal

from ui_system.interface import Interface, GraphicalModes
from gmap.gmap_enums import TileType


def draw_tile(x, y, glyph, sprite, char_color, render_order=None, background=None):
    if render_order:
        terminal.layer(render_order.value)
    if Interface.mode == GraphicalModes.ASCII:
        terminal.printf(x, y, f'[bkcolor={background}][color={char_color}]{glyph}[/color][/bkcolor]')
    elif Interface.mode == GraphicalModes.TILES:
        terminal.color(f'{char_color}')
        terminal.put(x, y, Interface.get_code(sprite))
    else:
        print(f'render camera: graphical mode {Interface.mode} not implemented.')
        raise NotImplementedError


def is_revealed_and_wall(gmap, x, y):
    idx = gmap.xy_idx(x, y)
    return gmap.tiles[idx] == TileType.WALL and gmap.revealed_tiles[idx]


def is_wall_around(gmap,x, y):
    idx = gmap.xy_idx(x, y)
    return gmap.tiles[idx] == TileType.WALL


def get_wall_glyph(idx, gmap):
    # sprite only
    x, y = gmap.index_to_point2d(idx)
    if x < 1 or x > gmap.width - 2 or y < 1 or y > gmap.height - 2:
        return 'map/wall_full.png'

    # On regarde autour du mur le contenu
    mask = 0
    if is_wall_around(gmap, x, y - 1):
        mask += 1
    if is_wall_around(gmap, x, y + 1):
        mask += 2
    if is_wall_around(gmap, x - 1, y):
        mask += 4
    if is_wall_around(gmap, x + 1, y):
        mask += 8

    if mask == 0:
        # no wall visible around : pillar.
        return 'map/wall_solo.png'
    elif mask == 1:
        # with a north wall
        return 'map/wall_north_w.png'
    elif mask == 2:
        # with a south wall
        return 'map/wall_south_w.png'
    elif mask == 3:
        # with a north & south wall
        return 'map/wall_north_south_w.png'
    elif mask == 4:
        # with west wall
        return 'map/wall_west_w.png'
    elif mask == 5:
        # with a west + north wall
        return 'map/wall_west_north_w.png'
    elif mask == 6:
        # with a west + south wall
        return 'map/wall_west_south_w.png'
    elif mask == 7:
        # with a west + north + south wall
        return 'map/wall_north_west_south_w.png'
    elif mask == 8:
        # with a east wall
        return 'map/wall_east_w.png'
    elif mask == 9:
        # with a east + north wall
        return 'map/wall_east_north_w.png'
    elif mask == 10:
        # with a east + south wall
        return 'map/wall_east_south_w.png'
    elif mask == 11:
        # with a east + north + south wall
        return 'map/wall_east_north_south_w.png'
    elif mask == 12:
        # with a east + west wall
        return 'map/wall_east_west_w.png'
    elif mask == 13:
        # with a east + west + north wall
        return 'map/wall_east_west_north_w.png'
    elif mask == 14:
        # with a east + west + south wall
        return 'map/wall_east_west_south_w.png'
    else:
        # full
        return 'map/wall_full.png'


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
        sprite = get_wall_glyph(idx, gmap)
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