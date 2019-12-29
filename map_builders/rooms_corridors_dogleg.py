from copy import deepcopy
from random import randint

from map_builders.builder_map import MetaMapbuilder
from map_builders.commons import apply_horizontal_tunnel, apply_vertical_tunnel


class DogLegCorridors(MetaMapbuilder):
    def build_meta_map(self, build_data):
        if build_data.rooms:
            rooms = deepcopy(build_data.rooms)
        else:
            print(f'DogLeg Corridors require a building with room structures')
            raise SystemError

        corridors = list()
        for i, room in enumerate(rooms):
            if i > 0:
                new_x, new_y = room.center()
                prev_x, prev_y = rooms[i - 1].center()
                if randint(0, 1) == 1:
                    c1 = apply_horizontal_tunnel(prev_x, new_x, prev_y, build_data.map)
                    c2 = apply_vertical_tunnel(prev_y, new_y, new_x, build_data.map)
                    c1.extend(c2)
                    corridors.append(c1)
                else:
                    c1 = apply_vertical_tunnel(prev_y, new_y, prev_x, build_data.map)
                    c2 = apply_horizontal_tunnel(prev_x, new_x, new_y, build_data.map)
                    c1.extend(c2)
                    corridors.append(c1)
                build_data.take_snapshot()
        build_data.corridors = corridors
