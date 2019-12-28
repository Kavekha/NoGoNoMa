from copy import deepcopy

from map_builders.builder_map import MetaMapbuilder
from map_builders.builder_structs import RoomSort


class RoomSorter(MetaMapbuilder):
    def build_meta_map(self, build_data):
        if build_data.rooms:
            rooms = deepcopy(build_data.rooms)
        else:
            print(f'RoomSorter require a building with room structures')
            raise SystemError

        sorted_by, *args = self.args

        if sorted_by == RoomSort.LEFTMOST:
            rooms = sorted(rooms, key=lambda sorted_room: sorted_room.x1)
        elif sorted_by == RoomSort.RIGHTMOST:
            rooms = sorted(rooms, key=lambda sorted_room: sorted_room.x2, reverse=True)
        elif sorted_by == RoomSort.TOPMOST:
            rooms = sorted(rooms, key=lambda sorted_room: sorted_room.y1)
        elif sorted_by == RoomSort.BOTTOMMOST:
            rooms = sorted(rooms, key=lambda sorted_room: sorted_room.y2, reverse=True)
        elif sorted_by == RoomSort.CENTRAL:
            map_center_x = build_data.map.width // 2
            map_center_y = build_data.map.height // 2
            room_center = list()
            for room in rooms:
                room_center.append((sorted_central(room, map_center_x, map_center_y), room))
            rooms_center = sorted(room_center, key=lambda sorted_room: sorted_room[0])
            new_rooms = list()
            for room in rooms_center:
                new_rooms.append(room[1])
            rooms = new_rooms

        build_data.rooms = rooms


def sorted_central(room, map_center_x, map_center_y):
    center_x, center_y = room.center()
    distance_to_x = abs(map_center_x - center_x)
    distance_to_y = abs(map_center_y - center_y)
    return distance_to_x + distance_to_y
