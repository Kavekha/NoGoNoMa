from map_builders.builder_map import MetaMapbuilder
from data.load_raws import RawsMaster
from gmap.spawner import spawn_room


class RoomBasedSpawner(MetaMapbuilder):
    def build_meta_map(self, build_data):
        if not build_data.rooms:
            print(f'Room based spawning only work after rooms have been created.')
            raise ProcessLookupError
        else:
            rooms = build_data.rooms
            build_data.map.spawn_table = RawsMaster.get_spawn_table_for_depth(build_data.map.depth)
            for room in rooms:
                if len(rooms) > 0 and room != rooms[0]:
                    spawn_room(room, build_data.map, build_data.spawn_list)
