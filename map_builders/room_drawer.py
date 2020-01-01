from copy import deepcopy
from random import randint
from itertools import product as it_product

from map_builders.builder_map import MetaMapbuilder
from map_builders.commons import distance_to
from gmap.gmap_enums import TileType


class RoomDrawer(MetaMapbuilder):
    def build_meta_map(self, build_data):
        if not build_data.rooms:
            print(f'Room based spawning only work after rooms have been created.')
            raise ProcessLookupError
        else:
            rooms = deepcopy(build_data.rooms)
            for room in rooms:
                if randint(1, 4) == 1:
                    self.draw_circle(build_data.map, room)
                else:
                    self.draw_rectangle(build_data.map, room)
                build_data.take_snapshot()

    def draw_rectangle(self, gmap, room):
        '''
        for y in range(room.y1, room.y2):
            for x in range(room.x1, room.x2):
                idx = gmap.xy_idx(x, y)
                if 0 < idx < ((gmap.width * gmap.height) - 1):
                    gmap.tiles[idx] = TileType.FLOOR
        '''
        for x, y in it_product(range(room.x1, room.x2), range(room.y1, room.y2)):
            idx = gmap.xy_idx(x, y)
            if 0 < idx < ((gmap.width * gmap.height) - 1):
                gmap.tiles[idx] = TileType.FLOOR

    def draw_circle(self, gmap, room):
        radius = min(room.x2 - room.x1, room.y2 - room.y1) / 2.0
        center_x, center_y = room.center()

        '''
        for y in range(room.y1, room.y2):
            for x in range(room.x1, room.x2):
                idx = gmap.xy_idx(x, y)
                distance = distance_to(x, y, center_x, center_y)
                if 0 < idx < (gmap.width * gmap.height) - 1 and distance < radius:
                    gmap.tiles[idx] = TileType.FLOOR
        '''
        for x, y in it_product(range(room.x1, room.x2), range(room.y1, room.y2)):
            idx = gmap.xy_idx(x, y)
            distance = distance_to(x, y, center_x, center_y)
            if 0 < idx < (gmap.width * gmap.height) - 1 and distance < radius:
                gmap.tiles[idx] = TileType.FLOOR
