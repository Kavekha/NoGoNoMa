import copy
from random import randint

from map_builders.builder_map import InitialMapBuilder
from map_builders.map_builders import Rect
from gmap.gmap_enums import TileType
import config


class BspInteriorMapBuilder(InitialMapBuilder):
    def __init__(self):
        self.rects = list()

    def build_initial_map(self, build_data):
        self.build(build_data)

    def build(self, build_data):
        self.rects.clear()
        self.rects.append(Rect(1, 1, build_data.map.width - 2, build_data.map.height - 2))
        first_room = self.rects[0]
        self.add_subrects(first_room)

        rooms = list()
        rooms_copy = copy.deepcopy(self.rects)
        for room in rooms_copy:
            rooms.append(room)
            for y in range(room.y1, room.y2):
                for x in range(room.x1, room.x2):
                    idx = build_data.map.xy_idx(x, y)
                    if 0 < idx < ((build_data.map.width * build_data.map.height) - 1):
                        build_data.map.tiles[idx] = TileType.FLOOR
            build_data.take_snapshot()

        build_data.rooms = rooms

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
