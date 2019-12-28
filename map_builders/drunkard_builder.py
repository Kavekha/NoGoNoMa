from random import randint

from map_builders.builder_map import InitialMapBuilder

from gmap.gmap_enums import TileType
from map_builders.builder_structs import DrunkSpawnMode, Symmetry
from map_builders.commons import paint


class DrunkardsWalkBuilder(InitialMapBuilder):
    def __init__(self, mode=DrunkSpawnMode.STARTING_POINT, lifetime=400, floor_percent=0.5):
        super().__init__()
        self.mode = mode
        self.lifetime = lifetime
        self.floor_percent = floor_percent
        self.noise_areas = dict()
        self.symmetry = Symmetry.NONE
        self.brush_size = 1

        if self.floor_percent > 0.9:
            print(f'floor percent at {self.floor_percent} : too high.')
            raise ValueError

    def build_map(self, build_data):
        # starting point
        x, y = build_data.map.width // 2, build_data.map.height // 2
        start_idx = build_data.map.xy_idx(x, y)

        total_tiles = build_data.map.width * build_data.map.height
        desired_floor_tiles = int(total_tiles * self.floor_percent)
        floor_tile_count = build_data.map.tiles.count(TileType.FLOOR)
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
                    drunk_x = randint(1, build_data.map.width - 3) + 1
                    drunk_y = randint(1, build_data.map.height - 3) + 1
                    drunk_idx = build_data.map.xy_idx(drunk_x, drunk_y)
            else:
                print(f'This DrunkSpawnMode is not implemented : {self.mode}')
                raise NotImplementedError

            while drunk_life > 0:
                if build_data.map.tiles[drunk_idx] == TileType.WALL:
                    did_something = True
                drunk_x, drunk_y = build_data.map.index_to_point2d(drunk_idx)
                paint(drunk_x, drunk_y, build_data.map, self.symmetry, self.brush_size)
                build_data.map.tiles[drunk_idx] = TileType.DOWN_STAIRS
                stagger_direction = randint(1, 4)
                if stagger_direction == 1 and drunk_x > 2:
                    drunk_x -= 1
                elif stagger_direction == 2 and drunk_x < build_data.map.width - 2:
                    drunk_x += 1
                elif stagger_direction == 3 and drunk_y > 2:
                    drunk_y -= 1
                elif stagger_direction == 4 and drunk_y < build_data.map.height - 2:
                    drunk_y += 1
                drunk_life -= 1
                drunk_idx = build_data.map.xy_idx(drunk_x, drunk_y)

            if did_something:
                build_data.take_snapshot()
                active_digger_count += 1

            digger_count += 1
            for i, tile in enumerate(build_data.map.tiles):
                if tile == TileType.DOWN_STAIRS:
                    build_data.map.tiles[i] = TileType.FLOOR

            floor_tile_count = build_data.map.tiles.count(TileType.FLOOR)

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
