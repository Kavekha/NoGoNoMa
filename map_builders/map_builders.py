from tcod import tcod

import copy

from gmap.gmap_enums import TileType
from gmap.utils import index_to_point2d, xy_idx
import config


class MapBuilder:
    def __init__(self, depth):
        self.map = Gmap(depth)
        self.starting_position = (0, 0)
        self.depth = depth
        self.history = list()
        self.map.create_fov_map()

    def reset(self):
        self.history = list()

    def get_snapshot_history(self):
        return self.history

    def take_snapshot(self):
        if config.SHOW_MAPGEN_VISUALIZER:
            snapshot = copy.deepcopy(self.map)
            snapshot.revealed_tiles = [True] * (snapshot.height * snapshot.width)
            snapshot.visible_tiles = [True] * (snapshot.height * snapshot.width)
            self.history.append(snapshot)

    def build_map(self):
        self.build()
        self.spawn_entities()
        self.map.populate_blocked()
        self.map.create_fov_map()

    def spawn_entities(self):
        raise NotImplementedError

    def get_map(self):
        return self.map

    def get_starting_position(self):
        return self.starting_position

    def build(self):
        raise NotImplementedError


class Gmap:
    def __init__(self, depth):
        self.tiles = [TileType.WALL] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.rooms = []

        self.width = config.MAP_WIDTH
        self.height = config.MAP_HEIGHT

        self.revealed_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.visible_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.blocked_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)

        self.tile_content = [[None] for x in range(config.MAP_HEIGHT * config.MAP_WIDTH)]
        self.depth = depth
        self.stains = [0] * (config.MAP_HEIGHT * config.MAP_WIDTH)

        self.fov_map = None
        self.spawn_table = None

    def create_fov_map(self):
        fov_map = tcod.tcod.map.Map(self.width, self.height)

        '''
        for i in range(0, len(self.tiles)):
            x, y = index_to_point2d(i)
            if self.tiles[i] != TileType.WALL:
                fov_map.walkable[y, x] = True  # Like the rest of the tcod modules, all arrays here are in row-major order and are addressed with [y,x]
                fov_map.transparent[y, x] = True
            else:
                fov_map.walkable[y, x] = False
                fov_map.transparent[y, x] = False
        '''
        for i, tile in enumerate(self.tiles):
            x, y = index_to_point2d(i)
            if tile != TileType.WALL:
                fov_map.walkable[y, x] = True  # Like the rest of the tcod modules, all arrays here are in row-major order and are addressed with [y,x]
                fov_map.transparent[y, x] = True
            else:
                fov_map.walkable[y, x] = False
                fov_map.transparent[y, x] = False

        self.fov_map = fov_map

        self.print_fov_map()

    def print_map(self):
        dic_map = {}
        for idx in range(len(self.tiles)):
            x, y = index_to_point2d(idx)
            try:
                dic_map[y]
            except:
                dic_map[y] = {}
            dic_map[y][x] = self.tiles[idx]

        map_string = ''
        for y, row in dic_map.items():
            map_y = ''
            for x, tile in row.items():
                tile = self.tiles[xy_idx(x, y)]
                if tile == TileType.DOWN_STAIRS:
                    map_y += '> '
                elif tile == TileType.FLOOR:
                    map_y += '. '
                elif tile == TileType.WALL:
                    map_y += '# '
                elif tile == TileType.EXIT_PORTAL:
                    map_y += 'O '
                else:
                    map_y += '* '
            map_string += '\n' + map_y
        print(f'\n{map_string}')

    def print_fov_map(self):
        print(f'FOV MAP TO PRINT !')
        map_string = ''
        for x in range(0, self.height - 1):
            map_x = ''
            for y in range(0, self.width - 1):
                if self.fov_map.walkable[x][y]:
                    map_x += '+ '
                else:
                    map_x += '# '
            map_string += map_x + '\n'

        print(map_string)

    def populate_blocked(self):
        for (i, tile) in enumerate(self.tiles):
            if tile == TileType.WALL:
                self.blocked_tiles[i] = True
            else:
                self.blocked_tiles[i] = False

    def clear_content_index(self):
        self.tile_content = [[] for x in range(config.MAP_HEIGHT * config.MAP_WIDTH)]


class Rect:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    def intersect(self, other):
        if self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1:
            return True
        return False

    def center(self):
        return (self.x1 + self.x2)//2, (self.y1 + self.y2) // 2
