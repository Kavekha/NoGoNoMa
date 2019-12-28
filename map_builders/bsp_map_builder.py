import copy
from random import randint

from map_builders.builder_map import InitialMapBuilder
from map_builders.map_builders import Rect
from map_builders.commons import apply_room_to_map, draw_corridor
from gmap.gmap_enums import TileType


class BspMapBuilder(InitialMapBuilder):
    def __init__(self):
        self.rects = list()

    def build_map(self, build_data):
        self.build(build_data)

    def build(self, build_data):
        rooms = list()
        self.rects.clear()
        self.rects.append(Rect(3, 3, build_data.map.width - 5, build_data.map.height - 5))
        first_room = self.rects[0]
        self.add_subrects(first_room)

        n_rooms = 0
        while n_rooms < 240:
            rect = self.get_random_rect()
            candidate = self.get_random_sub_rect(rect)

            if self.is_possible(candidate, build_data.map):
                apply_room_to_map(candidate, build_data.map)
                rooms.append(candidate)
                self.add_subrects(rect)
                build_data.take_snapshot()

            n_rooms += 1

        rooms = sorted(rooms, key=lambda sorted_room: sorted_room.x1)
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

    def add_subrects(self, rect):
        width = abs(rect.x1 - rect.x2)
        height = abs(rect.y1 - rect.y2)
        half_width = max(width // 2, 1)
        half_height = max(height // 2, 1)

        self.rects.append(Rect(rect.x1, rect.y1, half_width, half_height))
        self.rects.append(Rect(rect.x1, rect.y1 + half_height, half_width, half_height))
        self.rects.append(Rect(rect.x1 + half_width, rect.y1, half_width, half_height))
        self.rects.append(Rect(rect.x1 + half_width, rect.y1 + half_height, half_width, half_height))

    def get_random_rect(self):
        if len(self.rects) == 1:
            return self.rects[0]

        idx = randint(0, len(self.rects) - 1)
        return self.rects[idx]

    def get_random_sub_rect(self, rect):
        result = copy.deepcopy(rect)
        rect_width = abs(rect.x1 - rect.x2)
        rect_height = abs(rect.y1 - rect.y2)
        width = max(3, randint(1, min(rect_width, 10)) - 1) + 1
        height = max(3, randint(1, min(rect_height, 10)) - 1) + 1

        result.x1 += randint(1, 6) - 1
        result.y1 += randint(1, 6) - 1
        result.x2 = result.x1 + width
        result.y2 = result.y1 + height

        return result

    def is_possible(self, rect, gmap):
        expanded = copy.deepcopy(rect)
        expanded.x1 -= 2
        expanded.x2 += 2
        expanded.y1 -= 2
        expanded.y2 += 2
        can_build = True

        for y in range(expanded.y1, expanded.y2):
            for x in range(expanded.x1, expanded.x2):
                if x > gmap.width - 2 or y > gmap.height - 2 or x < 1 or y < 1:
                    can_build = False

                if can_build:
                    idx = gmap.xy_idx(x, y)
                    if gmap.tiles[idx] != TileType.WALL:
                        can_build = False

        return can_build
