import tcod

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


def return_most_distant_reachable_area(map, start_idx):
    x, y = start_idx
    map.populate_blocked()
    map.create_fov_map()
    dij_path = tcod.path.Dijkstra(map.fov_map, 1.41)

    # Compute path from starting position
    best_exit = 0
    best_distance = 0
    for (i, tile) in enumerate(map.tiles):
        if tile == TileType.FLOOR:
            exit_tile_x, exit_tile_y = map.index_to_point2d(i)
            dij_path.set_goal(exit_tile_x, exit_tile_y)
            my_path = dij_path.get_path(x, y)
            if my_path:
                if len(my_path) > best_distance:
                    best_exit = i
                    best_distance = len(my_path)

    if best_exit:
        return best_exit
    return False
