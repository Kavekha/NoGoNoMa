from map_builders.builder_map import MetaMapbuilder
from map_builders.commons import distance_to
from map_builders.builder_structs import StartX, StartY
from gmap.gmap_enums import TileType


class AreaStartingPosition(MetaMapbuilder):
    def build_meta_map(self, build_data):
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
