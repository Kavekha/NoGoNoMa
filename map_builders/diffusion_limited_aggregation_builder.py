from random import randint

import tcod as tcod

from map_builders.builder_map import InitialMapBuilder, MetaMapbuilder

from map_builders.builder_structs import DLAAlgorithm, Symmetry
from gmap.gmap_enums import TileType
from map_builders.commons import paint


class DLABuilder(InitialMapBuilder, MetaMapbuilder):
    def __init__(self):
        super().__init__()
        self.noise_areas = dict()
        self.algorithm = DLAAlgorithm.WALK_INWARDS
        self.symmetry = Symmetry.NONE
        self.brush_size = 1
        self.floor_percent = 0.25

    def build_meta_map(self, build_data):
        self.build_map(build_data)

    def build_initial_map(self, build_data):
        # starting point
        x, y = build_data.map.width // 2, build_data.map.height // 2
        start_idx = build_data.map.xy_idx(x, y)
        build_data.take_snapshot()

        build_data.map.tiles[start_idx] = TileType.FLOOR
        build_data.map.tiles[start_idx - 1] = TileType.FLOOR
        build_data.map.tiles[start_idx + 1] = TileType.FLOOR
        build_data.map.tiles[start_idx - build_data.map.width] = TileType.FLOOR
        build_data.map.tiles[start_idx + build_data.map.width] = TileType.FLOOR
        build_data.take_snapshot()

        # random walker
        total_tiles = build_data.map.width * build_data.map.height
        desired_floor_tiles = int(self.floor_percent * total_tiles)
        floor_tile_count = build_data.map.tiles.count(TileType.FLOOR)

        while floor_tile_count < desired_floor_tiles:
            if self.algorithm == DLAAlgorithm.WALK_INWARDS:
                digger_x = randint(1, build_data.map.width - 3) + 1
                digger_y = randint(1, build_data.map.height - 3) + 1
                digger_idx = build_data.map.xy_idx(digger_x, digger_y)
                prev_x = digger_x
                prev_y = digger_y

                while build_data.map.tiles[digger_idx] == TileType.WALL:
                    prev_x = digger_x
                    prev_y = digger_y
                    stagger_direction = randint(1, 4)
                    if stagger_direction == 1 and digger_x > 2:
                        digger_x -= 1
                    elif stagger_direction == 2 and digger_x < build_data.map.width - 2:
                        digger_x += 1
                    elif stagger_direction == 3 and digger_y > 2:
                        digger_y -= 1
                    elif stagger_direction == 4 and digger_y < build_data.map.height - 2:
                        digger_y += 1
                    digger_idx = build_data.map.xy_idx(digger_x, digger_y)
                paint(prev_x, prev_y, build_data.map, self.symmetry, self.brush_size)
            elif self.algorithm == DLAAlgorithm.WALK_OUTWARDS:
                digger_x = x
                digger_y = y
                digger_idx = build_data.map.xy_idx(digger_x, digger_y)
                while build_data.map.tiles[digger_idx] == TileType.FLOOR:
                    stagger_direction = randint(1, 4)
                    if stagger_direction == 1 and digger_x > 2:
                        digger_x -= 1
                    elif stagger_direction == 2 and digger_x < build_data.map.width - 2:
                        digger_x += 1
                    elif stagger_direction == 3 and digger_y > 2:
                        digger_y -= 1
                    elif stagger_direction == 4 and digger_y < build_data.map.height - 2:
                        digger_y += 1
                    digger_idx = build_data.map.xy_idx(digger_x, digger_y)
                paint(digger_x, digger_y, build_data.map, self.symmetry, self.brush_size)
            elif self.algorithm == DLAAlgorithm.CENTRAL_ATTRACTOR:
                digger_x = randint(1, build_data.map.width - 3) + 1
                digger_y = randint(1, build_data.map.height - 3) + 1
                digger_idx = build_data.map.xy_idx(digger_x, digger_y)
                prev_x = digger_x
                prev_y = digger_y

                where = tcod.line_where(digger_x, digger_y, x, y, inclusive=False)
                count = 0
                while build_data.map.tiles[digger_idx] == TileType.WALL and where:
                    prev_x = digger_x
                    prev_y = digger_y
                    digger_x = where[0][count]
                    digger_y = where[1][count]
                    digger_idx = build_data.map.xy_idx(digger_x, digger_y)
                    count += 1
                paint(prev_x, prev_y, build_data.map, self.symmetry, self.brush_size)
            else:
                print(f'Algorithm {self.algorithm} not implemented.')
                raise NotImplementedError
            floor_tile_count = build_data.map.tiles.count(TileType.FLOOR)
            if randint(0, 10) == 1:
                build_data.take_snapshot()

    def heavy_erosion(self):
        self.algorithm = DLAAlgorithm.WALK_INWARDS
        self.brush_size = 2
        self.symmetry = Symmetry.NONE
        self.floor_percent = 0.35
        return self

    def walk_inwards(self):
        self.algorithm = DLAAlgorithm.WALK_INWARDS
        self.symmetry = Symmetry.NONE
        self.brush_size = 1
        self.floor_percent = 0.25
        return self

    def walk_outwards(self):
        self.algorithm = DLAAlgorithm.WALK_OUTWARDS
        self.symmetry = Symmetry.NONE
        self.brush_size = 2
        self.floor_percent = 0.25
        return self

    def central_attractor(self):
        self.algorithm = DLAAlgorithm.CENTRAL_ATTRACTOR
        self.symmetry = Symmetry.NONE
        self.brush_size = 2
        self.floor_percent = 0.25
        return self

    def insectoid(self):
        self.algorithm = DLAAlgorithm.CENTRAL_ATTRACTOR
        self.symmetry = Symmetry.HORIZONTAL
        self.brush_size = 2
        self.floor_percent = 0.25
        return self
