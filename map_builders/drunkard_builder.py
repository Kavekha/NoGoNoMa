from random import randint

from map_builders.map_builders import MapBuilder
from gmap.gmap_enums import TileType
from map_builders.builder_structs import DrunkSpawnMode, Symmetry
from map_builders.commons import return_most_distant_reachable_area, generate_voronoi_spawn_points, paint
from gmap.spawner import spawn_region

import config


class DrunkardsWalkBuilder(MapBuilder):
    def __init__(self, depth, mode=DrunkSpawnMode.STARTING_POINT, lifetime=400, floor_percent=0.5):
        super().__init__(depth)
        self.mode = mode
        self.lifetime = lifetime
        self.floor_percent = floor_percent
        self.noise_areas = dict()
        self.symmetry = Symmetry.NONE
        self.brush_size = 1

        if self.floor_percent > 0.9:
            print(f'floor percent at {self.floor_percent} : too high.')
            raise ValueError

    def open_area(self):
        self.mode = DrunkSpawnMode.STARTING_POINT
        self.lifetime = 400
        self.floor_percent = 0.5
        return self

    def open_halls(self):
        self.mode = DrunkSpawnMode.RANDOM
        self.lifetime = 400
        self.floor_percent = 0.5
        return self

    def winding_passages(self):
        self.mode = DrunkSpawnMode.RANDOM
        self.lifetime = 100
        self.floor_percent = 0.4
        return self

    def fat_passages(self):
        self.mode = DrunkSpawnMode.RANDOM
        self.lifetime = 100
        self.floor_percent = 0.4
        self.brush_size = 2
        return self

    def fearfull_symmetry(self):
        self.mode = DrunkSpawnMode.RANDOM
        self.lifetime = 100
        self.floor_percent = 0.4
        self.brush_size = 1
        self.symmetry = Symmetry.BOTH
        return self

    def spawn_entities(self):
        for area in self.noise_areas:
            spawn_region(self.noise_areas[area], self.map)

    def build(self):
        # starting point
        x, y = self.map.width // 2, self.map.height // 2
        start_idx = self.map.xy_idx(x, y)
        self.starting_position = x, y

        total_tiles = self.map.width * self.map.height
        desired_floor_tiles = int(total_tiles * self.floor_percent)
        floor_tile_count = self.map.tiles.count(TileType.FLOOR)
        digger_count = 0
        active_digger_count = 0

        while floor_tile_count < desired_floor_tiles:
            did_something = False
            drunk_life = self.lifetime
            if self.mode == DrunkSpawnMode.STARTING_POINT:
                drunk_idx = start_idx
            elif self.mode == DrunkSpawnMode.RANDOM:
                if digger_count == 0:
                    drunk_idx = start_idx
                else:
                    drunk_x = randint(1, self.map.width - 3) + 1
                    drunk_y = randint(1, self.map.height - 3) + 1
                    drunk_idx = self.map.xy_idx(drunk_x, drunk_y)
            else:
                print(f'This DrunkSpawnMode is not implemented : {self.mode}')
                raise NotImplementedError

            while drunk_life > 0:
                if self.map.tiles[drunk_idx] == TileType.WALL:
                    did_something = True
                drunk_x, drunk_y = self.map.index_to_point2d(drunk_idx)
                paint(drunk_x, drunk_y, self.map, self.symmetry, self.brush_size)
                self.map.tiles[drunk_idx] = TileType.DOWN_STAIRS
                stagger_direction = randint(1, 4)
                if stagger_direction == 1 and drunk_x > 2:
                    drunk_x -= 1
                elif stagger_direction == 2 and drunk_x < self.map.width - 2:
                    drunk_x += 1
                elif stagger_direction == 3 and drunk_y > 2:
                    drunk_y -= 1
                elif stagger_direction == 4 and drunk_y < self.map.height - 2:
                    drunk_y += 1
                drunk_life -= 1
                drunk_idx = self.map.xy_idx(drunk_x, drunk_y)

            if did_something:
                self.take_snapshot()
                active_digger_count += 1

            digger_count += 1
            for i, tile in enumerate(self.map.tiles):
                if tile == TileType.DOWN_STAIRS:
                    self.map.tiles[i] = TileType.FLOOR

            floor_tile_count = self.map.tiles.count(TileType.FLOOR)

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