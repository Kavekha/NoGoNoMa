import tcod as tcod

from copy import deepcopy
from random import randint

from map_builders.builder_map import MetaMapbuilder
from gmap.gmap_enums import TileType
import config


class DistantExit(MetaMapbuilder):
    def build_meta_map(self, build_data):
        x, y = deepcopy(build_data.starting_position)

        build_data.map.populate_blocked()
        build_data.map.create_fov_map()
        dij_path = tcod.path.Dijkstra(build_data.map.fov_map, 1.41)

        # Compute path from starting position
        best_exit = 0
        best_distance = 0
        for (i, tile) in enumerate(build_data.map.tiles):
            if tile == TileType.FLOOR:
                exit_tile_x, exit_tile_y = build_data.map.index_to_point2d(i)
                dij_path.set_goal(exit_tile_x, exit_tile_y)
                my_path = dij_path.get_path(x, y)
                if my_path:
                    print(f'{i} my path len : {len(my_path)}')
                    # avoid always the best of the best
                    random_best = best_distance - randint(0, 1)
                    if len(my_path) > random_best or (len(my_path) == random_best and randint(0, 1) == 1):
                        best_exit = i
                        best_distance = len(my_path)


        if best_exit:
            print(f'best exit is : {best_exit} with distance {best_distance}')
            if build_data.map.depth != config.MAX_DEPTH:
                build_data.map.tiles[best_exit] = TileType.DOWN_STAIRS
            else:
                build_data.map.tiles[best_exit] = TileType.EXIT_PORTAL
        else:
            print('No exit found with Distant Exit')
            raise SystemError
