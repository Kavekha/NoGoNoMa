import copy
from random import randint

from map_builders.map_builders import MapBuilder, Rect
from gmap.utils import xy_idx
from gmap.gmap_enums import TileType
import config


class CellularAutomataBuilder(MapBuilder):
    def __init__(self, depth):
        super().__init__(depth)

    def spawn_entities(self):
        pass

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

        x, y = self.map.width // 2, self.map.height // 2
        start_idx = xy_idx(x, y)
        while self.map.tiles[start_idx] != TileType.FLOOR:
            x -= 1
            start_idx = xy_idx(x, y)
        self.starting_position = x, y

        import tcod
        from gmap.utils import index_to_point2d

        self.map.create_fov_map()
        fov = self.map.fov_map
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute path from starting position
        x, y = self.starting_position
        exit = False

        for (i, tile) in enumerate(self.map.tiles):
            if tile == TileType.FLOOR:
                exit_tile_x, exit_tile_y = index_to_point2d(i)
                tcod.path_compute(my_path, y, x, exit_tile_y, exit_tile_x)
                if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 500:
                    exit = True
                    if self.depth != config.MAX_DEPTH:
                        self.map.tiles[i] = TileType.DOWN_STAIRS
                    else:
                        self.map.tiles[i] = TileType.EXIT_PORTAL
                    tcod.path_delete(my_path)
                    self.take_snapshot()
                    self.take_snapshot()
                    self.take_snapshot()
                    self.take_snapshot()
                    break

        if not exit:
            print('no exit found')
            raise NotImplementedError

