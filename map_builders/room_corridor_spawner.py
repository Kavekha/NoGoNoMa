from copy import deepcopy

from map_builders.builder_map import MetaMapbuilder
from gmap.spawner import spawn_region
from map_builders.commons import distance_to, draw_corridor


class CorridorSpawner(MetaMapbuilder):
    def build_meta_map(self, build_data):
        if not build_data.corridors:
            print(f'Corridors based spawning only work after corridors have been created.')
            raise ProcessLookupError
        else:
            corridors = deepcopy(build_data.corridors)
            for corridor in corridors:
                spawn_region(corridor, build_data.map, build_data.spawn_list)
