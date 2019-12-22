import tcod

import copy
from random import randint

from map_builders.map_builders import MapBuilder
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
        self.map.create_fov_map()
        dij_path = tcod.path.Dijkstra(self.map.fov_map, 1.41)

        # Compute path from starting position
        best_exit = 0
        best_distance = 0
        for (i, tile) in enumerate(self.map.tiles):
            if tile == TileType.FLOOR:
                exit_tile_x, exit_tile_y = self.map.index_to_point2d(i)
                dij_path.set_goal(exit_tile_x, exit_tile_y)
                my_path = dij_path.get_path(x, y)
                if my_path:
                    if len(my_path) > best_distance:
                        best_exit = i
                        best_distance = len(my_path)

        if best_exit:
            if self.depth != config.MAX_DEPTH:
                self.map.tiles[best_exit] = TileType.DOWN_STAIRS
            else:
                self.map.tiles[best_exit] = TileType.EXIT_PORTAL

            # we can add starting position for player
            self.starting_position = x, y
            self.take_snapshot()

            # simili voronoi with noise

            noise = tcod.noise.Noise(
                dimensions=2,
                algorithm=tcod.NOISE_SIMPLEX,
                implementation=tcod.noise.TURBULENCE,
                hurst=0.5,
                lacunarity=2.0,
                octaves=4,
                seed=None
            )

            for y in range(0, self.map.height):
                for x in range(0, self.map.width):
                    if self.map.tiles[self.map.xy_idx(x, y)] == TileType.FLOOR:
                        # score between 0.99 & 0.5 : 550 at >0.9, 1200 at >8, 0 at > 6 and 200 at < 6.
                        cell_value = noise.get_point(x, y)
                        cell_value_int = int(cell_value * 10)       # so we have enought for 10 areas.
                        if cell_value_int not in self.noise_areas:
                            self.noise_areas[cell_value_int] = list()
                        self.noise_areas[cell_value_int].append(self.map.xy_idx(x, y))

            count = 0
            for key, value in self.noise_areas.items():
                print(f'area {key} - nb of points : {len(value)} idx')
                count += 1
            print(f'number of areas : {count}')

        else:
            print('WARNING: Cellula Automata - No exit found. Re-doing.')
            self.reset()
            self.build()
