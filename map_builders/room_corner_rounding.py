from copy import deepcopy

from map_builders.builder_map import MetaMapbuilder
from gmap.gmap_enums import TileType


class RoomCornerRounding(MetaMapbuilder):
    def build_meta_map(self, build_data):
        if build_data.rooms:
            rooms = deepcopy(build_data.rooms)
        else:
            print(f'Room exploder require a building with room structures')
            raise SystemError

        for room in rooms:
            self.fill_it_corner(room.x1, room.y1, build_data)
            self.fill_it_corner(room.x2, room.y1, build_data)
            self.fill_it_corner(room.x1, room.y2, build_data)
            self.fill_it_corner(room.x2, room.y2, build_data)

            build_data.take_snapshot()

    def fill_it_corner(self, corner_x, corner_y, build_data):
        width = build_data.map.width
        height = build_data.map.height
        idx = build_data.map.xy_idx(corner_x, corner_y)

        neighbor_walls = 0
        if corner_x > 0 and build_data.map.tiles[idx - 1] == TileType.WALL:
            neighbor_walls += 1
        if corner_y > 0 and build_data.map.tiles[idx - width] == TileType.WALL:
            neighbor_walls += 1
        if corner_x < width - 2 and build_data.map.tiles[idx + 1] == TileType.WALL:
            neighbor_walls += 1
        if corner_y < height - 2 and build_data.map.tiles[idx + width] == TileType.WALL:
            neighbor_walls += 1

        print(f'fill requested for {corner_x, corner_y}')
        if neighbor_walls == 2:
            print(f'{corner_x, corner_y} corner x, corner y has been rounder !')
            build_data.map.tiles[idx] = TileType.WALL
        else:
            print(f'no rounding for {corner_x, corner_y}')
