from tcod import tcod

from gmap.gmap_enums import TileType


class Gmap:
    def __init__(self, depth, width, height, name='DEFAULT_MAP_NAME'):
        self.depth = depth
        self.width = width
        self.height = height
        self.name = name

        self.tiles = [TileType.WALL] * (self.height * self.width)
        self.rooms = []

        self.revealed_tiles = [False] * (self.height * self.width)
        self.visible_tiles = [False] * (self.height * self.width)
        self.blocked_tiles = [False] * (self.height * self.width)
        self.view_blocked = dict()

        self.tile_content = [list() for x in range(self.height * self.width)]
        self.stains = [0] * (self.height * self.width)

        self.fov_map = None
        self.spawn_table = None

    def reset(self):
        self.tiles = [TileType.WALL] * (self.height * self.width)
        self.rooms = []

        self.revealed_tiles = [False] * (self.height * self.width)
        self.visible_tiles = [False] * (self.height * self.width)
        self.blocked_tiles = [False] * (self.height * self.width)
        self.view_blocked = dict()

        self.tile_content = [list() for x in range(self.height * self.width)]
        self.stains = [0] * (self.height * self.width)

        self.fov_map = None
        self.spawn_table = None

    def out_of_bound(self, idx):
        x, y = self.index_to_point2d(idx)
        if 0 > x > self.width - 1 or 0 > y > self.height - 1:
            return True
        return False

    def is_constructible_tile(self, idx):
        x, y = self.index_to_point2d(idx)
        if 1 > x > self.width - 2 or 1 > y > self.height - 2:
            return True
        return False

    def is_opaque(self, idx):
        if self.tiles[idx] == TileType.WALL or self.view_blocked.get(idx):
            return True

    def index_to_point2d(self, idx):
        # Transform an idx 1D array to a x, y format for 2D array
        return int(idx % self.width), idx // self.width

    def xy_idx(self, x, y):
        # Return the map tile (x, y). Avoid List in list [x][y]
        return (y * self.width) + x

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
        self.tile_content = [[] for x in range(self.height * self.width)]

