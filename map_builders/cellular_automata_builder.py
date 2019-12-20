import tcod

import copy
from random import randint

from gmap.utils import index_to_point2d
from map_builders.map_builders import MapBuilder, Rect
from gmap.utils import xy_idx
from gmap.gmap_enums import TileType
from gmap.spawner import spawn_region
import config


class CellularAutomataBuilder(MapBuilder):
    def __init__(self, depth):
        super().__init__(depth)

    def spawn_entities(self):
        # region of spawn points
        spawn_points = []
        tiles_check = 0
        for y in range(1, self.map.height - 2, randint(1, 3)):
            for x in range(1, self.map.width - 2):
                idx = xy_idx(x, y)
                if self.map.tiles[idx] == TileType.FLOOR:
                    tiles_check += 1
                    if randint(0, 3) == 1:
                        spawn_points.append(xy_idx(x, y))
                    if len(spawn_points) >= 3:
                        print(f'SPAWN: {spawn_points}')
                        spawn_region(spawn_points, self.map)
                        spawn_points = []

    def build(self):
        for y in range(1, self.map.height - 2):
            for x in range(1, self.map.width - 2):
                rand = randint(1, 100)
                idx = xy_idx(x, y)
                if rand > 55:
                    self.map.tiles[idx] = TileType.FLOOR
                else:
                    self.map.tiles[idx] = TileType.WALL

        self.take_snapshot()

        for _i in range(0, 15):
            newtiles = copy.deepcopy(self.map.tiles)

            for y in range(1, self.map.height -2):
                for x in range(1, self.map.width - 2):
                    idx = xy_idx(x, y)
                    neighbors = 0
                    if self.map.tiles[idx - 1] == TileType.WALL:
                        neighbors += 1
                    if self.map.tiles[idx + 1] == TileType.WALL:
                        neighbors += 1
                    if self.map.tiles[idx - self.map.width] == TileType.WALL:
                        neighbors += 1
                    if self.map.tiles[idx + self.map.width] == TileType.WALL:
                        neighbors += 1
                    if self.map.tiles[idx - (self.map.width + 1)] == TileType.WALL:
                        neighbors += 1
                    if self.map.tiles[idx - (self.map.width - 1)] == TileType.WALL:
                        neighbors += 1
                    if self.map.tiles[idx + (self.map.width + 1)] == TileType.WALL:
                        neighbors += 1
                    if self.map.tiles[idx + (self.map.width - 1)] == TileType.WALL:
                        neighbors += 1

                    if neighbors > 4 or neighbors == 0:
                        newtiles[idx] = TileType.WALL
                    else:
                        newtiles[idx] = TileType.FLOOR

            self.map.tiles = copy.deepcopy(newtiles)
            self.take_snapshot()

        # starting point
        x, y = self.map.width // 2, self.map.height // 2
        start_idx = xy_idx(x, y)
        while self.map.tiles[start_idx] != TileType.FLOOR:
            x -= 1
            start_idx = xy_idx(x, y)

        # Found an exit
        self.map.create_fov_map()
        fov = self.map.fov_map
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute path from starting position
        available_exits = []
        for (i, tile) in enumerate(self.map.tiles):
            if tile == TileType.FLOOR:
                exit_tile_x, exit_tile_y = index_to_point2d(i)
                tcod.path_compute(my_path, y, x, exit_tile_y, exit_tile_x)
                if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 500:
                    available_exits.append(i)

        tcod.path_delete(my_path)
        if available_exits:
            rand = randint(0, len(available_exits) - 1)
            if self.depth != config.MAX_DEPTH:
                self.map.tiles[rand] = TileType.DOWN_STAIRS
            else:
                self.map.tiles[rand] = TileType.EXIT_PORTAL

            # we can add starting position for player
            self.starting_position = x, y
            self.take_snapshot()

        else:
            print('WARNING: Cellula Automata - No exit found. Re-doing.')
            self.reset()
            self.build()
