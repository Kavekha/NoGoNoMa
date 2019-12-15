from random import randint

from map_builders.map_builders import MapBuilder, Gmap, Rect
from map_builders.commons import apply_room_to_map, apply_horizontal_tunnel, apply_vertical_tunnel
from gmap.utils import xy_idx
from gmap.gmap_enums import TileType
from gmap.spawner import spawn_room
from data.load_raws import RawsMaster
import config


class SimpleMapBuilder(MapBuilder):
    def build(self, depth):
        map = Gmap(depth)
        player_position = self.rooms_and_corridors(map)
        map.create_fov_map()
        return map, player_position

    def spawn(self, map, depth):
        map.spawn_table = RawsMaster.get_spawn_table_for_depth(depth)
        for room in map.rooms:
            if len(map.rooms) > 0 and room != map.rooms[0]:
                spawn_room(room, map)

    def rooms_and_corridors(self, map):
        MAX_ROOMS = 30
        MIN_SIZE = 6
        MAX_SIZE = 10

        for _i in range(0, MAX_ROOMS):
            w = randint(MIN_SIZE, MAX_SIZE)
            h = randint(MIN_SIZE, MAX_SIZE)
            x = randint(2, map.width - w - 1) -1
            y = randint(2, map.height - h - 1) -1
            new_room = Rect(x, y, w, h)

            can_be_add = True
            for other_room in map.rooms:
                if new_room.intersect(other_room):
                    can_be_add = False

            if can_be_add:
                apply_room_to_map(new_room, map)

                if map.rooms:
                    (new_x, new_y) = new_room.center()
                    (prev_x, prev_y) = map.rooms[len(map.rooms) -1].center()
                    if randint(0, 1) == 1:
                        apply_horizontal_tunnel(prev_x, new_x, prev_y, map)
                        apply_vertical_tunnel(prev_y, new_y, new_x,  map)
                    else:
                        apply_vertical_tunnel(prev_y, new_y, prev_x,  map)
                        apply_horizontal_tunnel(prev_x, new_x, new_y,  map)
                else:
                    print(f'new map: first room, with center {new_room.center()}')

                map.rooms.append(new_room)

        stair_position_x, stair_position_y = map.rooms[len(map.rooms) -1].center()
        stair_idx = xy_idx(stair_position_x, stair_position_y)
        print(f'self is {self} and have {self.__dict__}')
        if map.depth != config.MAX_DEPTH:
            map.tiles[stair_idx] = TileType.DOWN_STAIRS
        else:
            map.tiles[stair_idx] = TileType.EXIT_PORTAL

        start_position = map.rooms[0].center()
        return start_position
