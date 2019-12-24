from random import randint

import tcod as tcod

from map_builders.map_builders import MapBuilder
from map_builders.builder_structs import DLAAlgorithm, Symmetry
from gmap.gmap_enums import TileType
from map_builders.commons import return_most_distant_reachable_area, generate_voronoi_spawn_points, paint
from gmap.spawner import spawn_region

import config


class DLABuilder(MapBuilder):
    def __init__(self, depth):
        super().__init__(depth)
        self.noise_areas = dict()
        self.algorithm = DLAAlgorithm.WALK_INWARDS
        self.symmetry = Symmetry.NONE
        self.brush_size = 1
        self.floor_percent = 0.25

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

    def build(self):
        # starting point
        x, y = self.map.width // 2, self.map.height // 2
        start_idx = self.map.xy_idx(x, y)
        self.starting_position = x, y
        self.take_snapshot()

        self.map.tiles[start_idx] = TileType.FLOOR
        self.map.tiles[start_idx - 1] = TileType.FLOOR
        self.map.tiles[start_idx + 1] = TileType.FLOOR
        self.map.tiles[start_idx - self.map.width] = TileType.FLOOR
        self.map.tiles[start_idx + self.map.width] = TileType.FLOOR
        self.take_snapshot()

        # random walker
        total_tiles = self.map.width * self.map.height
        desired_floor_tiles = int(self.floor_percent * total_tiles)
        floor_tile_count = self.map.tiles.count(TileType.FLOOR)

        while floor_tile_count < desired_floor_tiles:
            if self.algorithm == DLAAlgorithm.WALK_INWARDS:
                digger_x = randint(1, self.map.width - 3) + 1
                digger_y = randint(1, self.map.height - 3) + 1
                digger_idx = self.map.xy_idx(digger_x, digger_y)
                prev_x = digger_x
                prev_y = digger_y

                while self.map.tiles[digger_idx] == TileType.WALL:
                    prev_x = digger_x
                    prev_y = digger_y
                    stagger_direction = randint(1, 4)
                    if stagger_direction == 1 and digger_x > 2:
                        digger_x -= 1
                    elif stagger_direction == 2 and digger_x < self.map.width - 2:
                        digger_x += 1
                    elif stagger_direction == 3 and digger_y > 2:
                        digger_y -= 1
                    elif stagger_direction == 4 and digger_y < self.map.height - 2:
                        digger_y += 1
                    digger_idx = self.map.xy_idx(digger_x, digger_y)
                paint(prev_x, prev_y, self.map, self.symmetry, self.brush_size)
            elif self.algorithm == DLAAlgorithm.WALK_OUTWARDS:
                digger_x = x
                digger_y = y
                digger_idx = self.map.xy_idx(digger_x, digger_y)
                while self.map.tiles[digger_idx] == TileType.FLOOR:
                    stagger_direction = randint(1, 4)
                    if stagger_direction == 1 and digger_x > 2:
                        digger_x -= 1
                    elif stagger_direction == 2 and digger_x < self.map.width - 2:
                        digger_x += 1
                    elif stagger_direction == 3 and digger_y > 2:
                        digger_y -= 1
                    elif stagger_direction == 4 and digger_y < self.map.height - 2:
                        digger_y += 1
                    digger_idx = self.map.xy_idx(digger_x, digger_y)
                paint(digger_x, digger_y, self.map, self.symmetry, self.brush_size)
            elif self.algorithm == DLAAlgorithm.CENTRAL_ATTRACTOR:
                digger_x = randint(1, self.map.width - 3) + 1
                digger_y = randint(1, self.map.height - 3) + 1
                digger_idx = self.map.xy_idx(digger_x, digger_y)
                prev_x = digger_x
                prev_y = digger_y

                where = tcod.line_where(digger_x, digger_y, x, y, inclusive=False)
                count = 0
                while self.map.tiles[digger_idx] == TileType.WALL and where:
                    prev_x = digger_x
                    prev_y = digger_y
                    digger_x = where[0][count]
                    digger_y = where[1][count]
                    digger_idx = self.map.xy_idx(digger_x, digger_y)
                    count += 1
                paint(prev_x, prev_y, self.map, self.symmetry, self.brush_size)
            else:
                print(f'Algorithm {self.algorithm} not implemented.')
                raise NotImplementedError
            floor_tile_count = self.map.tiles.count(TileType.FLOOR)
            if randint(0, 10) == 1:
                self.take_snapshot()

        best_exit = return_most_distant_reachable_area(self.map, start_idx)

        if best_exit:
            if self.depth != config.MAX_DEPTH:
                self.map.tiles[best_exit] = TileType.DOWN_STAIRS
            else:
                self.map.tiles[best_exit] = TileType.EXIT_PORTAL

            # we can add starting position for player
            self.starting_position = x, y
            self.take_snapshot()

            # simili voronoi with noise
            self.noise_areas = generate_voronoi_spawn_points(self.map)
            for area in self.noise_areas:
                spawn_region(self.noise_areas[area], self.map, self.spawn_list)
