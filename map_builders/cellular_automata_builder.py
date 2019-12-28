import copy
from random import randint

from map_builders.builder_map import InitialMapBuilder
from gmap.gmap_enums import TileType


class CellularAutomataBuilder(InitialMapBuilder):
    def __init__(self):
        super().__init__()
        self.noise_areas = dict()

    def build_map(self, build_data):
        self.build(build_data)

    def build(self, build_data):
        for y in range(1, build_data.map.height - 2):
            for x in range(1, build_data.map.width - 2):
                rand = randint(1, 100)
                idx = build_data.map.xy_idx(x, y)
                if rand > 55:
                    build_data.map.tiles[idx] = TileType.FLOOR
                else:
                    build_data.map.tiles[idx] = TileType.WALL

        build_data.take_snapshot()

        for _i in range(0, 15):
            newtiles = copy.deepcopy(build_data.map.tiles)

            for y in range(1, build_data.map.height -2):
                for x in range(1, build_data.map.width - 2):
                    idx = build_data.map.xy_idx(x, y)
                    neighbors = 0
                    if build_data.map.tiles[idx - 1] == TileType.WALL:
                        neighbors += 1
                    if build_data.map.tiles[idx + 1] == TileType.WALL:
                        neighbors += 1
                    if build_data.map.tiles[idx - build_data.map.width] == TileType.WALL:
                        neighbors += 1
                    if build_data.map.tiles[idx + build_data.map.width] == TileType.WALL:
                        neighbors += 1
                    if build_data.map.tiles[idx - (build_data.map.width + 1)] == TileType.WALL:
                        neighbors += 1
                    if build_data.map.tiles[idx - (build_data.map.width - 1)] == TileType.WALL:
                        neighbors += 1
                    if build_data.map.tiles[idx + (build_data.map.width + 1)] == TileType.WALL:
                        neighbors += 1
                    if build_data.map.tiles[idx + (build_data.map.width - 1)] == TileType.WALL:
                        neighbors += 1

                    if neighbors > 4 or neighbors == 0:
                        newtiles[idx] = TileType.WALL
                    else:
                        newtiles[idx] = TileType.FLOOR

            build_data.map.tiles = copy.deepcopy(newtiles)
            build_data.take_snapshot()
