import tcod

import math

from gmap.gmap_enums import TileType
from map_builders.builder_structs import Symmetry


def distance_to(self_position_x, self_position_y, other_position_x, other_position_y):
    dx = other_position_x - self_position_x
    dy = other_position_y - self_position_y
    return math.sqrt(dx ** 2 + dy ** 2)


def draw_corridor(gmap, x1, y1, x2, y2):
    x = x1
    y = y1

    while x != x2 or y != y2:
        if x < x2:
            x += 1
        elif x > x2:
            x -= 1
        elif y < y2:
            y += 1
        elif y > y2:
            y -= 1

        idx = gmap.xy_idx(x, y)
        gmap.tiles[idx] = TileType.FLOOR


def apply_room_to_map(room, map):
    print(f'apply room : {room}, with {room.x1}, {room.x2}, {room.y1, room.y2}')
    for y in range(room.y1, room.y2 + 1):
        for x in range(room.x1, room.x2 + 1):
            map.tiles[map.xy_idx(x, y)] = TileType.FLOOR


def apply_horizontal_tunnel(x1, x2, y, map):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        idx = map.xy_idx(x, y)
        if 0 < idx < map.width * map.height:
            map.tiles[idx] = TileType.FLOOR


def apply_vertical_tunnel(y1, y2, x, map):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        idx = map.xy_idx(x, y)
        if 0 < idx < map.width * map.height:
            map.tiles[idx] = TileType.FLOOR


def paint(x, y, gmap, symmetry=Symmetry.NONE, brush_size=1):
    if symmetry == Symmetry.NONE:
        apply_paint(x, y, gmap, brush_size)
    elif symmetry == Symmetry.HORIZONTAL:
        center_x = gmap.width // 2
        if x == center_x:
            apply_paint(x, y, gmap, brush_size)
        else:
            dist_x = abs(center_x - x)
            apply_paint(center_x + dist_x, y, gmap, brush_size)
            apply_paint(center_x - dist_x, y, gmap, brush_size)
    elif symmetry == Symmetry.VERTICAL:
        center_y = gmap.height // 2
        if y == center_y:
            apply_paint(x, y, gmap, brush_size)
        else:
            dist_y = abs(center_y - y)
            apply_paint(x, center_y + dist_y, gmap, brush_size)
            apply_paint(x, center_y - dist_y, gmap, brush_size)
    elif symmetry == Symmetry.BOTH:
        center_x = gmap.width // 2
        center_y = gmap.height // 2
        if x == center_x and y == center_y:
            apply_paint(x, y, gmap, brush_size)
        else:
            dist_x = abs(center_x - x)
            apply_paint(center_x + dist_x, y, gmap, brush_size)
            apply_paint(center_x - dist_x, y, gmap, brush_size)
            dist_y = abs(center_y - y)
            apply_paint(x, center_y + dist_y, gmap, brush_size)
            apply_paint(x, center_y - dist_y, gmap, brush_size)


def apply_paint(x, y, gmap, brush_size=1):
    if brush_size == 1:
        digger_idx = gmap.xy_idx(x, y)
        gmap.tiles[digger_idx] = TileType.FLOOR
    else:
        half_brush_size = int(brush_size // 2)
        for brush_y in range(y - half_brush_size, y + half_brush_size):
            for brush_x in range(x - half_brush_size, x + half_brush_size):
                if 1 < brush_x < gmap.width - 1 and 1 < brush_y < gmap.height - 1:
                    idx = gmap.xy_idx(brush_x, brush_y)
                    gmap.tiles[idx] = TileType.FLOOR
