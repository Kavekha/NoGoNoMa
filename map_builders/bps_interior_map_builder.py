import copy
from random import randint

from map_builders.builder_map import InitialMapBuilder
from map_builders.commons import draw_corridor
from map_builders.map_builders import Rect
from gmap.gmap_enums import TileType
import config


class BspInteriorMapBuilder(InitialMapBuilder):
    def __init__(self):
        self.rects = list()

    def build_map(self, build_data):
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

        for i in range(0, len(rooms) - 1):
            room = rooms[i]
            next_room = rooms[i + 1]

            start_x = room.x1 + randint(1, abs(room.x1 - room.x2) - 1)
            start_y = room.y1 + randint(1, abs(room.y1 - room.y2) - 1)
            end_x = next_room.x1 + randint(1, abs(next_room.x1 - next_room.x2) - 1)
            end_y = next_room.y1 + randint(1, abs(next_room.y1 - next_room.y2) - 1)

            draw_corridor(build_data.map, start_x, start_y, end_x, end_y)
            build_data.take_snapshot()

        build_data.rooms = rooms

    '''
    def old(self):
        self.starting_position = self.rooms[0].center()

        stair_position_x, stair_position_y = self.rooms[len(self.rooms) - 1].center()
        stair_idx = self.map.xy_idx(stair_position_x, stair_position_y)

        if self.depth != config.MAX_DEPTH:
            self.map.tiles[stair_idx] = TileType.DOWN_STAIRS
        else:
            self.map.tiles[stair_idx] = TileType.EXIT_PORTAL

        self.starting_position = self.rooms[0].center()

        # fill spawn list
        self.map.spawn_table = RawsMaster.get_spawn_table_for_depth(self.depth)
        for room in self.rooms:
            if len(self.rooms) > 0 and room != self.rooms[0]:
                spawn_room(room, self.map, self.spawn_list)
    '''

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
