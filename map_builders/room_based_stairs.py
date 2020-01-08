import config
from map_builders.builder_map import MetaMapbuilder
from gmap.gmap_enums import TileType


class RoomBasedStairs(MetaMapbuilder):
    def build_meta_map(self, build_data):
        if not build_data.rooms:
            print(f'Room based spawning only work after rooms have been created.')
            raise ProcessLookupError
        else:
            rooms = build_data.rooms
            stair_position_x, stair_position_y = rooms[len(rooms) - 1].center()

            stair_idx = build_data.map.xy_idx(stair_position_x, stair_position_y)
            build_data.exit_position = (stair_position_x, stair_position_y)

            if build_data.map.depth != config.MAX_DEPTH:
                build_data.map.tiles[stair_idx] = TileType.DOWN_STAIRS
            else:
                build_data.map.tiles[stair_idx] = TileType.EXIT_PORTAL
            build_data.take_snapshot()