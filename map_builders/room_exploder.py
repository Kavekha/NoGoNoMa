from copy import deepcopy
from random import randint

from map_builders.builder_map import MetaMapbuilder
from map_builders.commons import paint
from map_builders.builder_structs import Symmetry
from gmap.gmap_enums import TileType


class RoomExploder(MetaMapbuilder):
    def build_meta_map(self, build_data):
        if build_data.rooms:
            rooms = deepcopy(build_data.rooms)
        else:
            print(f'Room exploder require a building with room structures')
            raise SystemError

        for room in rooms:
            start_x, start_y = room.center()
            n_diggers = randint(1, 20) - 5
            if n_diggers > 0:
                for _i in range(0, n_diggers):
                    drunk_x = start_x
                    drunk_y = start_y

                    drunk_life = 20
                    did_something = False

                    while drunk_life > 0:
                        drunk_idx = build_data.map.xy_idx(drunk_x, drunk_y)
                        if build_data.map.tiles[drunk_idx] == TileType.WALL:
                            did_something = True
                        paint(build_data.map, Symmetry.NONE, 1, drunk_x, drunk_y)
                        build_data.map.tiles[drunk_idx] = TileType.DOWN_STAIRS # for builder snapshot

                        stagger_direction = randint(1, 4)
                        if stagger_direction == 1 and drunk_x > 2:
                            drunk_x -= 1
                        elif stagger_direction == 2 and drunk_x < build_data.map.width - 2:
                            drunk_x += 1
                        elif stagger_direction == 3 and drunk_y > 2:
                            drunk_y -= 1
                        elif stagger_direction == 4 and drunk_y < build_data.map.height - 2:
                            drunk_y += 1

                        drunk_life -= 1

                    if did_something:
                        build_data.take_snapshot()

                        # apres snapshot, on rchange la tile en Floor comme souhaité à l'origine.
                        for i, tile in enumerate(build_data.map.tiles):
                            if tile == TileType.DOWN_STAIRS:
                                build_data.map.tiles[i] = TileType.FLOOR

                    # pour le dernier batch
                    for i, tile in enumerate(build_data.map.tiles):
                        if tile == TileType.DOWN_STAIRS:
                            build_data.map.tiles[i] = TileType.FLOOR
