import tcod as tcod
import math

from map_builders.builder_map import MetaMapbuilder
from map_builders.commons import distance_to
from gmap.gmap_enums import TileType, StartX, StartY


class AreaStartingPosition(MetaMapbuilder):
    '''
    def build_map(self, build_data):
        pass
    '''

    def build_map(self, build_data):
        start_x, start_y = self.args
        self.build(build_data, start_x, start_y)

    def build(self, build_data, start_x, start_y):
        if start_x == StartX.LEFT:
            x = 1
        elif start_x == StartX.CENTER:
            x = build_data.map.width // 2
        elif start_x == StartX.RIGHT:
            x = build_data.map.width - 2
        else:
            print('AreaStartingPosition : wrong type of Start X')
            raise NotImplementedError

        if start_y == StartY.TOP:
            y = 1
        elif start_y == StartY.CENTER:
            y = build_data.map.height // 2
        elif start_y == StartY.BOTTOM:
            y = build_data.map.height - 2
        else:
            print('AreaStartingPosition : wrong type of Start Y')
            raise NotImplementedError

        available_floors = list()

        for idx, tile in enumerate(build_data.map.tiles):
            if tile == TileType.FLOOR:
                closest_x, closest_y = build_data.map.index_to_point2d(idx)
                available_floors.append((idx, distance_to(x, y, closest_x, closest_y)))

        available_floors = sorted(available_floors, key=lambda floor: floor[1])

        new_x, new_y = build_data.map.index_to_point2d(available_floors[0][0])
        build_data.starting_position = new_x, new_y
        print(f'area: starting pos is {build_data.starting_position} and tile is {build_data.map.tiles[available_floors[0][0]]}')


        '''
        build_data.map.populate_blocked()
        build_data.map.create_fov_map()
        dij_path = tcod.path.Dijkstra(build_data.map.fov_map, 1.41)

        best_starting_point = build_data.map.xy_idx(x, y)
        print(f'original starting point is : {x}, {y}. tile is {build_data.map.tiles[best_starting_point]}')
        closest_distance = 999
        for (i, tile) in enumerate(build_data.map.tiles):
            if tile == TileType.FLOOR:
                closest_x, closest_y = build_data.map.index_to_point2d(i)
                dij_path.set_goal(closest_x, closest_y)
                my_path = dij_path.get_path(x, y)
                if my_path:
                    if len(my_path) < closest_distance:
                        best_starting_point = i
                        closest_distance = len(my_path)

        if closest_distance:
            new_x, new_y = build_data.map.index_to_point2d(best_starting_point)
            build_data.starting_position = new_x, new_y
            build_data.take_snapshot()
            print(f'area: starting position newx, newy is {new_x, new_y}. : tile is {build_data.map.tiles[best_starting_point]}')
            print(f'build data starting position is {build_data.starting_position}')
        else:
            print('AreaStartingPosition : No starting position found')
            raise SystemError
        '''
