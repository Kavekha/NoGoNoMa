from random import randint

from map_builders.simple_map_builder import SimpleMapBuilder
from map_builders.bsp_map_builder import BspMapBuilder


def random_builder(depth):
    rand = randint(0, 1)
    if rand == 0:
        return SimpleMapBuilder(depth)
    else:
        return BspMapBuilder(depth)


def build_random_map(depth):
    map_builder = random_builder(depth)
    map_builder.build_map()
    return map_builder

