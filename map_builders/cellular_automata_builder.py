import copy
from random import randint

from map_builders.builder_map import InitialMapBuilder
from map_builders.commons import return_most_distant_reachable_area, generate_voronoi_spawn_points
from gmap.gmap_enums import TileType
import config
from gmap.spawner import spawn_region



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

    '''
    def old(self):
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

            # simili voronoi with noise for spawn

            self.noise_areas = generate_voronoi_spawn_points(self.map)
            for area in self.noise_areas:
                spawn_region(self.noise_areas[area], self.map, self.spawn_list)


        else:
            print('WARNING: Cellula Automata - No exit found. Re-doing.')
            self.reset()
            self.build()
    '''
