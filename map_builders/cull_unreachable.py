import tcod as tcod

from copy import deepcopy
from map_builders.builder_map import MetaMapbuilder
from gmap.gmap_enums import TileType


class CullUnreachable(MetaMapbuilder):
    def build_map(self, build_data):
        x, y = deepcopy(build_data.starting_position)
        print(f'cull unreachable : starting position : {build_data.starting_position}. X, y  : {x, y}')

        start_idx = build_data.map.xy_idx(x, y)
        print(f'start idx is {start_idx}')
        build_data.map.populate_blocked()
        build_data.map.create_fov_map()
        dij_path = tcod.path.Dijkstra(build_data.map.fov_map, 1.41)

        for (i, tile) in enumerate(build_data.map.tiles):
            print(f'culling : i is {i}, tile is {tile}')
            if tile == TileType.FLOOR:
                if i == start_idx:
                    print(f'is start idx')
                else:
                    print(f'i is not star idx')
                    starting_distance = i
                    exit_tile_x, exit_tile_y = build_data.map.index_to_point2d(starting_distance)
                    dij_path.set_goal(exit_tile_x, exit_tile_y)
                    my_path = dij_path.get_path(x, y)
                    if not my_path:
                        print(f'cull unreachable cant found path to {exit_tile_x, exit_tile_y}')
                        build_data.map.tiles[i] = TileType.WALL
