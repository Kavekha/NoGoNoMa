import tcod

from random import randint

import config
from data.types import TileType

class Gmap:
    def __init__(self):
        self.rooms = []
        self.width = config.MAP_WIDTH
        self.height = config.MAP_HEIGHT
        self.tiles = self.new_map()
        self.fov_map = self.create_fov_map()
        self.revealed_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.visible_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.blocked_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
        self.tile_content = [[] for x in range(config.MAP_HEIGHT * config.MAP_WIDTH)]

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
        # TODO : Room out of map
        for y in range(room.y1, room.y2-1):
            for x in range(room.x1, room.x2-1):
                gmap[self.xy_idx(x, y)] = TileType.FLOOR

    def apply_horizontal_tunnel(self, x1, x2, y, gmap):
        for x in range(min(x1, x2), max(x1, x2)):
            idx = self.xy_idx(x, y)
            if idx > 0 and idx < config.MAP_WIDTH * config.MAP_HEIGHT:
                gmap[idx] = TileType.FLOOR

    def apply_vertical_tunnel(self, y1, y2, x, gmap):
        for y in range(min(y1, y2), max(y1, y2)):
            idx = self.xy_idx(x, y)
            if idx > 0 and idx < config.MAP_WIDTH * config.MAP_HEIGHT:
                gmap[idx] = TileType.FLOOR

    def new_map(self):
        # map filed with wall
        gmap = [TileType.WALL] * (config.MAP_HEIGHT * config.MAP_WIDTH)

        for _i in range(0, config.MAX_ROOMS):
            w = randint(config.MIN_SIZE, config.MAX_SIZE)
            h = randint(config.MIN_SIZE, config.MAX_SIZE)
            x = randint(1, config.MAP_WIDTH - w - 1) -1
            y = randint(1, config.MAP_HEIGHT - h - 1) -1
            new_room = Rect(x, y, w, h)

            can_be_add = True
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    can_be_add = False

            if can_be_add:
                self.apply_room_to_map(new_room, gmap)

                if self.rooms:
                    (new_x, new_y) = new_room.center()
                    (prev_x, prev_y) = self.rooms[len(self.rooms) -1].center()
                    if randint(0, 1) == 1:
                        self.apply_horizontal_tunnel(prev_x, new_x, prev_y, gmap)
                        self.apply_vertical_tunnel(prev_y, new_y, new_x, gmap)
                    else:
                        self.apply_vertical_tunnel(prev_y, new_y, prev_x, gmap)
                        self.apply_horizontal_tunnel(prev_x, new_x, new_y, gmap)

                self.rooms.append(new_room)

        return gmap


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
        return ((self.x1 + self.x2)//2, (self.y1 + self.y2) //2)


'''
def new_map_first_iteration():
    # map filed with floor
    gmap = [TileType.FLOOR] * (config.MAP_HEIGHT * config.MAP_WIDTH)

    # map with boundaries walls
    for x in range(config.MAP_WIDTH):
        gmap[xy_idx(x, 0)] = TileType.WALL
        gmap[xy_idx(x, config.MAP_HEIGHT -1)] = TileType.WALL

    for y in range(0, config.MAP_HEIGHT-1):
        gmap[xy_idx(0, y)] = TileType.WALL
        gmap[xy_idx(config.MAP_WIDTH-1, y)] = TileType.WALL

    # random walls
    from random import randint
    for _i in range(0, 400):
        x = randint(1, config.MAP_WIDTH -1)
        y = randint(1, config.MAP_HEIGHT -1)
        tile_pos = xy_idx(x, y)
        if tile_pos != xy_idx(config.BASE_PLAYER_X, config.BASE_PLAYER_Y):
            gmap[tile_pos] = TileType.WALL

    return gmap
'''
