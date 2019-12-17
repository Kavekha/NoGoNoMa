from random import randint

from map_builders.map_builders import MapBuilder, Gmap, Rect
from map_builders.commons import apply_room_to_map, apply_horizontal_tunnel, apply_vertical_tunnel
from gmap.utils import xy_idx
from gmap.gmap_enums import TileType
from gmap.spawner import spawn_room
from data.load_raws import RawsMaster
import config


class SimpleMapBuilder(MapBuilder):
    def __init__(self, depth):
        super().__init__(depth)
        self.rooms = list()

    def build(self):
        self.rooms_and_corridors()

    def spawn_entities(self):
        self.map.spawn_table = RawsMaster.get_spawn_table_for_depth(self.depth)
        for room in self.rooms:
            if len(self.rooms) > 0 and room != self.rooms[0]:
                spawn_room(room, self.map)

    def rooms_and_corridors(self):
        MAX_ROOMS = 30
        MIN_SIZE = 6
        MAX_SIZE = 10

        for _i in range(0, MAX_ROOMS):
            w = randint(MIN_SIZE, MAX_SIZE)
            h = randint(MIN_SIZE, MAX_SIZE)
            x = randint(2, self.map.width - w - 1) -1
            y = randint(2, self.map.height - h - 1) -1
            new_room = Rect(x, y, w, h)

            can_be_add = True
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    can_be_add = False

            if can_be_add:
                apply_room_to_map(new_room, self.map)

                if self.rooms:
                    (new_x, new_y) = new_room.center()
                    (prev_x, prev_y) = self.rooms[len(self.rooms) -1].center()
                    if randint(0, 1) == 1:
                        apply_horizontal_tunnel(prev_x, new_x, prev_y, self.map)
                        apply_vertical_tunnel(prev_y, new_y, new_x,  self.map)
                    else:
                        apply_vertical_tunnel(prev_y, new_y, prev_x,  self.map)
                        apply_horizontal_tunnel(prev_x, new_x, new_y,  self.map)
                else:
                    print(f'new map: first room, with center {new_room.center()}')

                self.rooms.append(new_room)
                self.take_snapshot()

        stair_position_x, stair_position_y = self.rooms[len(self.rooms) -1].center()
        stair_idx = xy_idx(stair_position_x, stair_position_y)
        if self.depth != config.MAX_DEPTH:
            self.map.tiles[stair_idx] = TileType.DOWN_STAIRS
        else:
            self.map.tiles[stair_idx] = TileType.EXIT_PORTAL

        self.starting_position = self.rooms[0].center()
