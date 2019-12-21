from gmap.gmap_enums import TileType


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
