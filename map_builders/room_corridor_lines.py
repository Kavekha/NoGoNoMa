import tcod as tcod

from copy import deepcopy
from random import randint

from map_builders.builder_map import MetaMapbuilder
from map_builders.commons import distance_to
from gmap.gmap_enums import TileType


class CorridorLines(MetaMapbuilder):
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
                    lines = tcod.line_where(room_x, room_y, dest_center_x, dest_center_y)
                    cell_x = lines[0]
                    cell_y = lines[1]
                    last_x = cell_x[0]
                    last_y = cell_y[0]

                    corridor = list()
                    for cell in range(0, len(cell_y) - 1):
                        if last_x != cell_x[cell] and last_y != cell_y[cell]:
                            if randint(1, 2) == 1:
                                idx = build_data.map.xy_idx(cell_x[cell], last_y)
                                build_data.map.tiles[idx] = TileType.FLOOR
                            else:
                                idx = build_data.map.xy_idx(last_x, cell_y[cell])
                                build_data.map.tiles[idx] = TileType.FLOOR
                        idx = int(build_data.map.xy_idx(cell_x[cell], cell_y[cell]))
                        build_data.map.tiles[idx] = TileType.FLOOR
                        last_x = cell_x[cell]
                        last_y = cell_y[cell]
                        corridor.append(idx)

                    corridors.append(corridor)
                    connected[i] = True
                    build_data.take_snapshot()

            build_data.corridors = corridors
