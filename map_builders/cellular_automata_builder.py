import tcod

import copy
from random import randint

from map_builders.map_builders import MapBuilder
from map_builders.commons import return_most_distant_reachable_area, generate_voronoi_spawn_points
from gmap.gmap_enums import TileType
from gmap.spawner import spawn_region
import config


class CellularAutomataBuilder(MapBuilder):
    def __init__(self, depth):
        super().__init__(depth)
        self.noise_areas = dict()

    def spawn_entities(self):
        for area in self.noise_areas:
            spawn_region(self.noise_areas[area], self.map)

    def build(self):
        for y in range(1, self.map.height - 2):
            for x in range(1, self.map.width - 2):
                rand = randint(1, 100)
                idx = self.map.xy_idx(x, y)
                if rand > 55:
                    self.map.tiles[idx] = TileType.FLOOR
                else:
                    self.map.tiles[idx] = TileType.WALL

        self.take_snapshot()

        for _i in range(0, 15):
            newtiles = copy.deepcopy(self.map.tiles)

            for y in range(1, self.map.height -2):
                for x in range(1, self.map.width - 2):
                    idx = self.map.xy_idx(x, y)
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
        start_idx = self.map.xy_idx(x, y)
        while self.map.tiles[start_idx] != TileType.FLOOR:
            x += 1
            y += 1
            start_idx = self.map.xy_idx(x, y)
        print(f'starting point is {start_idx}, {x, y}')

        # Found an exit
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

        else:
            print('WARNING: Cellula Automata - No exit found. Re-doing.')
            self.reset()
            self.build()
