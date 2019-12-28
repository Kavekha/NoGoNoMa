from random import randint

from map_builders.builder_map import InitialMapBuilder
from map_builders.map_builders import Rect
from map_builders.commons import apply_room_to_map, apply_horizontal_tunnel, apply_vertical_tunnel


class SimpleMapBuilder(InitialMapBuilder):
    def build_map(self, build_data):
        self.rooms_and_corridors(build_data)

    def rooms_and_corridors(self, build_data):
        MAX_ROOMS = 30
        MIN_SIZE = 6
        MAX_SIZE = 10
        rooms = list()

        for _i in range(0, MAX_ROOMS):
            w = randint(MIN_SIZE, MAX_SIZE)
            h = randint(MIN_SIZE, MAX_SIZE)
            x = randint(2, build_data.map.width - w - 1) -1
            y = randint(2, build_data.map.height - h - 1) -1
            new_room = Rect(x, y, w, h)

            can_be_add = True
            for other_room in rooms:
                if new_room.intersect(other_room):
                    can_be_add = False

            if can_be_add:
                apply_room_to_map(new_room, build_data.map)
                build_data.take_snapshot()

                if rooms:
                    (new_x, new_y) = new_room.center()
                    (prev_x, prev_y) = rooms[len(rooms) -1].center()
                    if randint(0, 1) == 1:
                        apply_horizontal_tunnel(prev_x, new_x, prev_y, build_data.map)
                        apply_vertical_tunnel(prev_y, new_y, new_x,  build_data.map)
                    else:
                        apply_vertical_tunnel(prev_y, new_y, prev_x,  build_data.map)
                        apply_horizontal_tunnel(prev_x, new_x, new_y,  build_data.map)
                else:
                    print(f'new map: first room, with center {new_room.center()}')

                rooms.append(new_room)
                build_data.take_snapshot()
        build_data.rooms = rooms
