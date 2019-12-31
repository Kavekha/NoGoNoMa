from copy import deepcopy
from random import randint

from map_builders.builder_map import MetaMapbuilder
from gmap.gmap_enums import TileType


class DoorPlacement(MetaMapbuilder):
    def __init__(self):
        super().__init__()
        self.doors = list()

    def build_meta_map(self, build_data):
        if build_data.corridors:
            corridors = deepcopy(build_data.corridors)
            for corridor in corridors:
                if len(corridor) > 2:
                    count = 0
                    while True:
                        if self.door_possible(build_data, corridor[count]):
                            build_data.spawn_list.append((corridor[count], "DOOR"))
                            break
                        else:
                            count += 1
                            if count > len(corridor) - 1:
                                break
        else:
            tiles = deepcopy(build_data.map.tiles)
            for i, tile in enumerate(tiles):
                if tile == TileType.FLOOR and self.door_possible(build_data, i) and randint(1, 3) == 1:
                    build_data.spawn_list.append((i, "DOOR"))

    def door_possible(self, build_data, idx):
        x = idx % build_data.map.width
        y = idx // build_data.map.width

        for spawn in build_data.spawn_list:
            if spawn[0] == idx:
                return False

        # East West door possibility
        if build_data.map.tiles[idx] == TileType.FLOOR and (x > 1 and build_data.map.tiles[idx - 1] == TileType.FLOOR) \
                and (x < build_data.map.width - 2 and build_data.map.tiles[idx + 1] == TileType.FLOOR) \
                and (y > 1 and build_data.map.tiles[idx - build_data.map.width] == TileType.WALL) \
                and (y < build_data.map.height - 2
                     and build_data.map.tiles[idx + build_data.map.width] == TileType.WALL):
            return True

        # North south door possibility
        if build_data.map.tiles[idx] == TileType.FLOOR and (x > 1 and build_data.map.tiles[idx - 1] == TileType.WALL) \
                and (x < build_data.map.width - 2 and build_data.map.tiles[idx + 1] == TileType.WALL) \
                and (y > 1 and build_data.map.tiles[idx - build_data.map.width] == TileType.FLOOR) \
                and (y < build_data.map.height - 2
                     and build_data.map.tiles[idx + build_data.map.width] == TileType.FLOOR):
            return True

        return False
