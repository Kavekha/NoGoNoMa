from random import randint

from map_builders.simple_map_builder import SimpleMapBuilder
from map_builders.bsp_map_builder import BspMapBuilder
from map_builders.bps_interior_map_builder import BspInteriorMapBuilder
from map_builders.cellular_automata_builder import CellularAutomataBuilder


def random_builder(depth):
    rand = 1  #randint(0, 3)
    if rand == 0:
        return BspInteriorMapBuilder(depth)
    elif rand == 1:
        return SimpleMapBuilder(depth)
    elif rand == 2:
        return BspMapBuilder(depth)
    elif rand == 3:
        return CellularAutomataBuilder(depth)
    else:
        return CellularAutomataBuilder(depth)


def build_random_map(depth):
    map_builder = random_builder(depth)
    map_builder.build_map()
    return map_builder

