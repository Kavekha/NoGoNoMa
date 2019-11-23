from bearlibterminal import terminal

from data.types import TileType
from world import World
from components.player_component import PlayerComponent
from components.viewshed_component import ViewshedComponent
import config


def draw_map():
    subjects = World.get_components(PlayerComponent, ViewshedComponent)
    if not subjects:
        return

    current_map = World.fetch('current_map')
    gmap = current_map.tiles
    for entity in subjects:
        terminal.layer(1)
        x = 0
        y = 0
        for tile in range(len(gmap)):
            if current_map.revealed_tiles[current_map.xy_idx(x, y)]:
                if current_map.visible_tiles[current_map.xy_idx(x, y)]:
                    if gmap[tile] == TileType.FLOOR:
                        terminal.printf(x, y, f'[color=dark yellow].[/color]')
                    elif gmap[tile] == TileType.WALL:
                        terminal.printf(x, y, f'[color=darker yellow]#[/color]')
                else:
                    if gmap[tile] == TileType.FLOOR:
                        terminal.printf(x, y, f'[color=dark gray].[/color]')
                    elif gmap[tile] == TileType.WALL:
                        terminal.printf(x, y, f'[color=darker gray]#[/color]')
            # Move coordinates
            x += 1
            if x > config.MAP_WIDTH - 1:
                x = 0
                y += 1


def draw_map_old():
    current_map = World.fetch('current_map')
    gmap = current_map.tiles

    terminal.layer(1)
    x = 0
    y = 0
    for tile in range(len(gmap)):
        if gmap[tile] == TileType.FLOOR:
            terminal.printf(x, y, f'[color=darker blue].[/color]')
        elif gmap[tile] == TileType.WALL:
            terminal.printf(x, y, f'[color=darker red]#[/color]')
        x += 1
        if x > config.MAP_WIDTH - 1:
            x = 0
            y += 1