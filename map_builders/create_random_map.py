from random import randint

from map_builders.simple_map_builder import SimpleMapBuilder
from map_builders.bsp_map_builder import BspMapBuilder
from map_builders.bps_interior_map_builder import BspInteriorMapBuilder


def random_builder(depth):
    rand = randint(0, 2)
    if rand == 0:
        return BspInteriorMapBuilder(depth)
    elif rand == 1:
        return SimpleMapBuilder(depth)
    elif rand == 2:
        return BspMapBuilder(depth)
    else:
        return BspInteriorMapBuilder(depth)


def build_random_map(depth):
    map_builder = random_builder(depth)
    map_builder.build_map()
    return map_builder

