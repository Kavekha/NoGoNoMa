import copy
from random import randint

from map_builders.map_builders import MapBuilder, Rect
from map_builders.commons import apply_room_to_map
from gmap.gmap_enums import TileType
from gmap.spawner import spawn_room
from data.load_raws import RawsMaster
import config


class BspMapBuilder(MapBuilder):
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
        self.rects.append(Rect(3, 3, self.map.width - 5, self.map.height - 5))
        first_room = self.rects[0]
        print(f'first room is : {first_room}, with {first_room.x1, first_room.x2} and {first_room.y1, first_room.y2}')
        self.add_subrects(first_room)
        print(f'rects is now : {self.rects}')

        n_rooms = 0
        while n_rooms < 240:
            rect = self.get_random_rect()
            candidate = self.get_random_sub_rect(rect)
            print(f'candidate is {candidate}')

            if self.is_possible(candidate):
                print(f'candidate will be room {candidate}')
                apply_room_to_map(candidate, self.map)
                self.rooms.append(candidate)
                self.add_subrects(rect)
                self.take_snapshot()
                print(f'rect list contains : {self.rects}')
            else:
                print(f'candidate {candidate} invalide')

            n_rooms += 1

        self.rooms = sorted(self.rooms, key=lambda room: room.x1)
        for i in range(0, len(self.rooms) - 1):
            room = self.rooms[i]
            next_room = self.rooms[i + 1]

            start_x = room.x1 + randint(1, abs(room.x1 - room.x2) - 1)
            start_y = room.y1 + randint(1, abs(room.y1 - room.y2) - 1)
            end_x = next_room.x1 + randint(1, abs(next_room.x1 - next_room.x2) - 1)
            end_y = next_room.y1 + randint(1, abs(next_room.y1 - next_room.y2) - 1)

            self.draw_corridor(start_x, start_y, end_x, end_y)
            self.take_snapshot()

        stair_position_x, stair_position_y = self.rooms[len(self.rooms) - 1].center()
        stair_idx = self.map.xy_idx(stair_position_x, stair_position_y)

        if self.depth != config.MAX_DEPTH:
            self.map.tiles[stair_idx] = TileType.DOWN_STAIRS
        else:
            self.map.tiles[stair_idx] = TileType.EXIT_PORTAL

        self.starting_position = self.rooms[0].center()

    def draw_corridor(self, x1, y1, x2, y2):
        x = x1
        y = y1

        while x != x2 or y != y2:
            if x < x2:
                x += 1
            elif x > x2:
                x -= 1
            elif y < y2:
                y += 1
            elif y > y2:
                y -= 1

            idx = self.map.xy_idx(x, y)
            self.map.tiles[idx] = TileType.FLOOR

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

    def is_possible(self, rect):
        expanded = copy.deepcopy(rect)
        expanded.x1 -= 2
        expanded.x2 += 2
        expanded.y1 -= 2
        expanded.y2 += 2
        can_build = True

        for y in range(expanded.y1, expanded.y2):
            for x in range(expanded.x1, expanded.x2):
                if x > self.map.width - 2 or y > self.map.height - 2 or x < 1 or y < 1:
                    can_build = False

                if can_build:
                    idx = self.map.xy_idx(x, y)
                    if self.map.tiles[idx] != TileType.WALL:
                        can_build = False

        return can_build
