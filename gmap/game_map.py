import tcod

from random import randint

import config
from gmap.gmap_enums import TileType


class Gmap:
    def __init__(self, depth):
        self.rooms = []
        self.width = config.MAP_WIDTH
        self.height = config.MAP_HEIGHT
        self.revealed_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.visible_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.blocked_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.tile_content = [[] for x in range(config.MAP_HEIGHT * config.MAP_WIDTH)]
        self.depth = depth
        self.stains = [0] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.tiles = self.new_map()
        self.fov_map = self.create_fov_map()
        self.spawn_table = None
        self.print_map_debug()

    def print_map_debug(self):
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

    def xy_idx(self, x, y):
        # Return the map tile (x, y). Avoid List in list [x][y]
        return (y * config.MAP_WIDTH) + x

    def index_to_point2d(self, idx):
        # Transform an idx 1D array to a x, y format for 2D array
        return idx % config.MAP_WIDTH, idx // config.MAP_WIDTH

    def clear_content_index(self):
        self.tile_content = [[] for x in range(config.MAP_HEIGHT * config.MAP_WIDTH)]

    def populate_blocked(self):
        for (i, tile) in enumerate(self.tiles):
            if tile == TileType.WALL:
                self.blocked_tiles[i] = True
            else:
                self.blocked_tiles[i] = False

    def create_fov_map(self):
        fov_map = tcod.map.Map(config.MAP_WIDTH, config.MAP_HEIGHT)

        for _i in range(len(self.tiles) - 1):
            if self.tiles[_i] != TileType.WALL:
                x, y = self.index_to_point2d(_i)
                fov_map.walkable[y, x] = True  # Like the rest of the tcod modules, all arrays here are in row-major order and are addressed with [y,x]
                fov_map.transparent[y, x] = True

        return fov_map

    def apply_room_to_map(self, room, gmap):
        for y in range(room.y1, room.y2-1):
            for x in range(room.x1, room.x2-1):
                gmap[self.xy_idx(x, y)] = TileType.FLOOR

    def apply_horizontal_tunnel(self, x1, x2, y, gmap):
        for x in range(min(x1, x2), max(x1, x2)):
            idx = self.xy_idx(x, y)
            if 0 < idx < config.MAP_WIDTH * config.MAP_HEIGHT:
                gmap[idx] = TileType.FLOOR

    def apply_vertical_tunnel(self, y1, y2, x, gmap):
        for y in range(min(y1, y2), max(y1, y2)):
            idx = self.xy_idx(x, y)
            if 0 < idx < config.MAP_WIDTH * config.MAP_HEIGHT:
                gmap[idx] = TileType.FLOOR

    def new_map(self):
        # map filed with wall
        tiles = [TileType.WALL] * (config.MAP_HEIGHT * config.MAP_WIDTH)

        for _i in range(0, config.MAX_ROOMS):
            w = randint(config.MIN_SIZE, config.MAX_SIZE)
            h = randint(config.MIN_SIZE, config.MAX_SIZE)
            x = randint(2, config.MAP_WIDTH - w - 1) -1
            y = randint(2, config.MAP_HEIGHT - h - 1) -1
            new_room = Rect(x, y, w, h)

            can_be_add = True
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    can_be_add = False

            if can_be_add:
                self.apply_room_to_map(new_room, tiles)

                if self.rooms:
                    (new_x, new_y) = new_room.center()
                    (prev_x, prev_y) = self.rooms[len(self.rooms) -1].center()
                    if randint(0, 1) == 1:
                        self.apply_horizontal_tunnel(prev_x, new_x, prev_y, tiles)
                        self.apply_vertical_tunnel(prev_y, new_y, new_x, tiles)
                    else:
                        self.apply_vertical_tunnel(prev_y, new_y, prev_x, tiles)
                        self.apply_horizontal_tunnel(prev_x, new_x, new_y, tiles)
                else:
                    print(f'new map: first room, with center {new_room.center()}')

                self.rooms.append(new_room)

        stair_position_x, stair_position_y = self.rooms[len(self.rooms) -1].center()
        stair_idx = self.xy_idx(stair_position_x, stair_position_y)
        print(f'self is {self} and have {self.__dict__}')
        if self.depth != config.MAX_DEPTH:
            tiles[stair_idx] = TileType.DOWN_STAIRS
        else:
            tiles[stair_idx] = TileType.EXIT_PORTAL

        return tiles


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
