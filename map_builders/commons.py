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


def return_most_distant_reachable_area(gmap, start_idx):
    x, y = gmap.index_to_point2d(start_idx)
    gmap.populate_blocked()
    gmap.create_fov_map()
    dij_path = tcod.path.Dijkstra(gmap.fov_map, 1.41)

    # Compute path from starting position
    best_exit = 0
    best_distance = 0
    for (i, tile) in enumerate(gmap.tiles):
        if tile == TileType.FLOOR:
            exit_tile_x, exit_tile_y = gmap.index_to_point2d(i)
            dij_path.set_goal(exit_tile_x, exit_tile_y)
            my_path = dij_path.get_path(x, y)
            if my_path:
                if len(my_path) > best_distance:
                    best_exit = i
                    best_distance = len(my_path)

    if best_exit:
        return best_exit
    return False


def generate_voronoi_spawn_points(gmap):
    noise = tcod.noise.Noise(
        dimensions=2,
        algorithm=tcod.NOISE_SIMPLEX,
        implementation=tcod.noise.TURBULENCE,
        hurst=0.5,
        lacunarity=2.0,
        octaves=4,
        seed=None
    )

    noise_areas = dict()
    for y in range(0, gmap.height):
        for x in range(0, gmap.width):
            if gmap.tiles[gmap.xy_idx(x, y)] == TileType.FLOOR:
                # score between 0.99 & 0.5 : 550 at >0.9, 1200 at >8, 0 at > 6 and 200 at < 6.
                cell_value = noise.get_point(x, y)
                cell_value_int = int(cell_value * 10)  # so we have enought for 10 areas.
                if cell_value_int not in noise_areas:
                    noise_areas[cell_value_int] = list()
                noise_areas[cell_value_int].append(gmap.xy_idx(x, y))

    count = 0
    for key, value in noise_areas.items():
        print(f'area {key} - nb of points : {len(value)} idx')
        count += 1
    print(f'number of areas : {count}')

    return noise_areas
