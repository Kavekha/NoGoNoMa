from copy import deepcopy
from random import randint

from map_builders.builder_map import MetaMapbuilder
from map_builders.commons import draw_corridor


class BSPCorridors(MetaMapbuilder):
    def build_meta_map(self, build_data):
        if build_data.rooms:
            rooms = deepcopy(build_data.rooms)
        else:
            print(f'BSP corridors require a building with room structures')
            raise SystemError

        corridors = list()
        for i in range(0, len(rooms) - 1):
            room = rooms[i]
            next_room = rooms[i + 1]

            start_x = room.x1 + randint(1, abs(room.x1 - room.x2) - 1)
            start_y = room.y1 + randint(1, abs(room.y1 - room.y2) - 1)
            end_x = next_room.x1 + randint(1, abs(next_room.x1 - next_room.x2) - 1)
            end_y = next_room.y1 + randint(1, abs(next_room.y1 - next_room.y2) - 1)

            corridor = draw_corridor(build_data.map, start_x, start_y, end_x, end_y)
            corridors.append(corridor)
            build_data.take_snapshot()
        build_data.corridors = corridors
