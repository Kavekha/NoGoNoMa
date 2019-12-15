from tcod import tcod
import config
from gmap.gmap_enums import TileType
from gmap.utils import index_to_point2d


class MapBuilder:
    pass

    def build(self, depth):
        raise NotImplementedError

    def spawn(self, map, depth):
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

        for _i in range(len(self.tiles) - 1):
            print(f'create fov map: tile is {self.tiles[_i]}')
            if self.tiles[_i] != TileType.WALL:
                x, y = index_to_point2d(_i)
                fov_map.walkable[y, x] = True  # Like the rest of the tcod modules, all arrays here are in row-major order and are addressed with [y,x]
                fov_map.transparent[y, x] = True
                print(f'fov map set : {fov_map.walkable[y, x]}')

        self.fov_map = fov_map

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
        return (self.x1 + self.x2)//2, (self.y1 + self.y2) //2