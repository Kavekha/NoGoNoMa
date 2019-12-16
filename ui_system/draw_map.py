from bearlibterminal import terminal

from ui_system.ui_enums import Layers
from gmap.gmap_enums import TileType
from gmap.utils import xy_idx
from world import World
from components.player_component import PlayerComponent
from components.viewshed_component import ViewshedComponent
from ui_system.interface import Interface, GraphicalModes
import config


def draw_map(map_to_draw):
    print(f'draw map requested')
    # current_map = World.fetch('current_map')
    tiles = map_to_draw.tiles

    if Interface.mode == GraphicalModes.ASCII:
        draw_map_ascii(map_to_draw, tiles)
    elif Interface.mode == GraphicalModes.TILES:
        draw_map_tiles(map_to_draw, tiles)


def draw_map_ascii(map_to_draw, tiles):
    terminal.layer(Layers.MAP.value)
    x = 0
    y = 0
    for tile in range(len(tiles)):
        if map_to_draw.revealed_tiles[map_to_draw.xy_idx(x, y)]:
            if map_to_draw.visible_tiles[map_to_draw.xy_idx(x, y)]:
                if tiles[tile] == TileType.FLOOR:
                    terminal.printf(x, y, f'[color=dark yellow].[/color]')
                elif tiles[tile] == TileType.WALL:
                    terminal.printf(x, y, f'[color=darker yellow]#[/color]')
                elif tiles[tile] == TileType.DOWN_STAIRS:
                    terminal.printf(x, y, f'[color=lighter blue]>[/color]')
                elif tiles[tile] == TileType.EXIT_PORTAL:
                    terminal.printf(x, y, f'[color=lighter blue]O[/color]')
            else:
                if tiles[tile] == TileType.FLOOR:
                    terminal.printf(x, y, f'[color=dark gray].[/color]')
                elif tiles[tile] == TileType.WALL:
                    terminal.printf(x, y, f'[color=darker gray]#[/color]')
                elif tiles[tile] == TileType.DOWN_STAIRS:
                    terminal.printf(x, y, f'[color=darker gray]>[/color]')
                elif tiles[tile] == TileType.EXIT_PORTAL:
                    terminal.printf(x, y, f'[color=darker gray]O[/color]')
            if map_to_draw.stains[tile]:
                terminal.printf(x, y, f'[bkcolor=red] [/color]')
        # Move coordinates
        x += 1
        if x > config.MAP_WIDTH - 1:
            x = 0
            y += 1


def draw_map_tiles(map_to_draw, tiles):
    terminal.layer(Layers.MAP.value)
    x = 0
    y = 0
    for tile in range(len(tiles)):
        if map_to_draw.revealed_tiles[xy_idx(x, y)]:
            if map_to_draw.visible_tiles[xy_idx(x, y)]:
                terminal.composition(terminal.TK_ON)
                if tiles[tile] == TileType.FLOOR:
                    terminal.color('dark yellow')
                    terminal.put(x, y, Interface.get_code('map/ground.png'))
                elif tiles[tile] == TileType.WALL:
                    terminal.color('darker yellow')
                    terminal.put(x, y, Interface.get_code('map/wall1.png'))
                elif tiles[tile] == TileType.DOWN_STAIRS:
                    terminal.color('lighter blue')
                    terminal.put(x, y, Interface.get_code('map/stairs_down.png'))
                elif tiles[tile] == TileType.EXIT_PORTAL:
                    terminal.color('lighter cyan')
                    terminal.put(x, y, Interface.get_code('map/stairs_down.png'))

                # blood stains
                if map_to_draw.stains[tile]:
                    terminal.layer(Layers.STAINS.value)
                    terminal.color('dark red')
                    terminal.put(x, y, Interface.get_code(f'/props/blood{map_to_draw.stains[tile]}.png'))
                terminal.composition(terminal.TK_OFF)
            else:
                if tiles[tile] == TileType.FLOOR:
                    terminal.color('dark gray')
                    terminal.put(x, y, Interface.get_code('map/ground.png'))
                elif tiles[tile] == TileType.WALL:
                    terminal.color('darker gray')
                    terminal.put(x, y, Interface.get_code('map/wall1.png'))
                elif tiles[tile] == TileType.DOWN_STAIRS:
                    terminal.color('dark gray')
                    terminal.put(x, y, Interface.get_code('map/stairs_down.png'))
                elif tiles[tile] == TileType.EXIT_PORTAL:
                    terminal.color('dark gray')
                    terminal.put(x, y, Interface.get_code('map/stairs_down.png'))

        # Move coordinates
        x += 1
        if x > config.MAP_WIDTH - 1:
            x = 0
            y += 1