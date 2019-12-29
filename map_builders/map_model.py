from tcod import tcod

from gmap.gmap_enums import TileType
import config


class Gmap:
    def __init__(self, depth):
        self.tiles = [TileType.WALL] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.rooms = []

        self.width = config.MAP_WIDTH
        self.height = config.MAP_HEIGHT

        self.revealed_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.visible_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.blocked_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.view_blocked = dict()

        self.tile_content = [[None] for x in range(config.MAP_HEIGHT * config.MAP_WIDTH)]
        self.depth = depth
        self.stains = [0] * (config.MAP_HEIGHT * config.MAP_WIDTH)

        self.fov_map = None
        self.spawn_table = None

    def is_opaque(self, idx):
        print(f'is opaque: {idx} : tile : {self.tiles[idx]} and get blocked: {self.view_blocked.get(idx)}')
        if self.tiles[idx] == TileType.WALL or self.view_blocked.get(idx):
            return True

    def index_to_point2d(self, idx):
        # Transform an idx 1D array to a x, y format for 2D array
        return int(idx % config.MAP_WIDTH), idx // config.MAP_WIDTH

    def xy_idx(self, x, y):
        # Return the map tile (x, y). Avoid List in list [x][y]
        return (y * config.MAP_WIDTH) + x

    def create_fov_map(self):
        fov_map = tcod.tcod.map.Map(self.width, self.height)

        for i, tile in enumerate(self.tiles):
            x, y = self.index_to_point2d(i)
            if tile != TileType.WALL:
                fov_map.walkable[
                    y, x] = True  # Like the rest of the tcod modules, all arrays here are in row-major order and are addressed with [y,x]
                if self.is_opaque(i):
                    fov_map.transparent[y, x] = False
                else:
                    fov_map.transparent[y, x] = True
            else:
                fov_map.walkable[y, x] = False
                fov_map.transparent[y, x] = False

        self.fov_map = fov_map

        self.print_fov_map()

    def print_map(self):
        dic_map = {}
        for idx in range(len(self.tiles)):
            x, y = self.index_to_point2d(idx)
            try:
                dic_map[y]
            except:
                dic_map[y] = {}
            dic_map[y][x] = self.tiles[idx]

        map_string = ''
        for y, row in dic_map.items():
            map_y = ''
            for x, tile in row.items():
                tile = self.tiles[self.xy_idx(x, y)]
                if tile == TileType.DOWN_STAIRS:
                    map_y += '>'
                elif tile == TileType.FLOOR:
                    map_y += '.'
                elif tile == TileType.WALL:
                    map_y += '#'
                elif tile == TileType.EXIT_PORTAL:
                    map_y += 'O'
                else:
                    map_y += '*'
            map_string += '\n' + map_y
        print(f'\n{map_string}')

    def print_fov_map(self):
        print(f'FOV MAP TO PRINT !')
        map_string = ''
        for x in range(0, self.height - 1):
            map_x = ''
            for y in range(0, self.width - 1):
                if self.fov_map.walkable[x][y]:
                    map_x += '+'
                else:
                    map_x += '#'
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

