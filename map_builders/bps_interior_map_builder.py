import copy
from random import randint

from map_builders.map_builders import MapBuilder, Rect
from gmap.utils import xy_idx
from gmap.gmap_enums import TileType
from data.load_raws import RawsMaster
from gmap.spawner import spawn_room
import config


class BspInteriorMapBuilder(MapBuilder):
    def __init__(self, depth):
        super().__init__(depth)
        self.rooms = list()
        self.rects = list()

    def spawn_entities(self):
        self.map.spawn_table = RawsMaster.get_spawn_table_for_depth(self.depth)
        for room in self.rooms:
            if len(self.rooms) > 0 and room != self.rooms[0]:
                spawn_room(room, self.map)

    def build(self):
        self.rects.clear()
        self.rects.append(Rect(1, 1, self.map.width - 2, self.map.height - 2))
        first_room = self.rects[0]
        self.add_subrects(first_room)

        rooms = copy.deepcopy(self.rects)
        for room in rooms:
            self.rooms.append(room)
            for y in range(room.y1, room.y2):
                for x in range(room.x1, room.x2):
                    idx = xy_idx(x, y)
                    if 0 < idx < ((self.map.width * self.map.height) - 1):
                        self.map.tiles[idx] = TileType.FLOOR
            self.take_snapshot()

        for i in range(0, len(self.rooms) - 1):
            room = self.rooms[i]
            next_room = self.rooms[i + 1]

            start_x = room.x1 + randint(1, abs(room.x1 - room.x2) - 1)
            start_y = room.y1 + randint(1, abs(room.y1 - room.y2) - 1)
            end_x = next_room.x1 + randint(1, abs(next_room.x1 - next_room.x2) - 1)
            end_y = next_room.y1 + randint(1, abs(next_room.y1 - next_room.y2) - 1)

            self.draw_corridor(start_x, start_y, end_x, end_y)
            self.take_snapshot()

        self.starting_position = self.rooms[0].center()

        stair_position_x, stair_position_y = self.rooms[len(self.rooms) - 1].center()
        stair_idx = xy_idx(stair_position_x, stair_position_y)

        if self.depth != config.MAX_DEPTH:
            self.map.tiles[stair_idx] = TileType.DOWN_STAIRS
        else:
            self.map.tiles[stair_idx] = TileType.EXIT_PORTAL

        self.starting_position = self.rooms[0].center()

    def draw_corridor(self, x1, y1, x2, y2):
        x = x1
        y = y1
        idx = xy_idx(x, y)
        self.map.tiles[idx] = TileType.DOWN_STAIRS

        while x != x2 or y != y2:
            if x < x2:
                x += 1
            elif x > x2:
                x -= 1
            elif y < y2:
                y += 1
            elif y > y2:
                y -= 1

            idx = xy_idx(x, y)
            self.map.tiles[idx] = TileType.FLOOR

        idx = xy_idx(x, y)
        self.map.tiles[idx] = TileType.EXIT_PORTAL

    def add_subrects(self, rect):
        if self.rects:
            self.rects.remove(self.rects[len(self.rects) - 1])

        width = rect.x2 - rect.x1
        height = rect.y2 - rect.y1
        half_width = width // 2
        half_height = height // 2

        split = randint(0, 1)
        if split == 0:
            h1 = Rect(rect.x1, rect.y1, half_width - 1, height)
            self.rects.append(h1)
            if half_width > config.MIN_SIZE:
                self.add_subrects(h1)
            h2 = Rect(rect.x1 + half_width, rect.y1, half_width, height)
            self.rects.append(h2)
            if half_width > config.MIN_SIZE:
                self.add_subrects(h2)
        else:
            v1 = Rect(rect.x1, rect.y1, width, half_height - 1)
            self.rects.append(v1)
            if half_height > config.MIN_SIZE:
                self.add_subrects(v1)
            v2 = Rect(rect.x1, rect.y1 + half_height, width, half_height)
            self.rects.append(v2)
            if half_height > config.MIN_SIZE:
                self.add_subrects(v2)
