from map_builders.builder_map import MetaMapbuilder


class RoomBasedStartingPosition(MetaMapbuilder):
    def build_meta_map(self, build_data):
        if not build_data.rooms:
            print(f'Room based spawning only work after rooms have been created.')
            raise ProcessLookupError
        else:
            rooms = build_data.rooms
            build_data.starting_position = rooms[0].center()
