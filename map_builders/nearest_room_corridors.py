from copy import deepcopy

from map_builders.builder_map import MetaMapbuilder
from map_builders.commons import distance_to, draw_corridor


class NearestCorridor(MetaMapbuilder):
    def build_meta_map(self, build_data):
        if not build_data.rooms:
            print(f'Room based spawning only work after rooms have been created.')
            raise ProcessLookupError
        else:
            rooms = deepcopy(build_data.rooms)
            connected = dict()

            corridors = list()
            for i, room in enumerate(rooms):
                room_distance = list()
                room_x, room_y = room.center()
                for j, other_room in enumerate(rooms):
                    if i != j and not connected.get(j):
                        other_x, other_y = other_room.center()
                        distance = distance_to(room_x, room_y, other_x, other_y)
                        room_distance.append((j, distance))

                if room_distance:
                    room_distance = sorted(room_distance, key=lambda room_to_sort: room_to_sort[1])
                    dest_center_x, dest_center_y = rooms[room_distance[0][0]].center()
                    corridor = draw_corridor(build_data.map, room_x, room_y, dest_center_x, dest_center_y)
                    connected[i] = True
                    build_data.take_snapshot()
                    corridors.append(corridor)

            build_data.corridors = corridors
