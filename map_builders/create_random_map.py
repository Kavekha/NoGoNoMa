from random import randint

from map_builders.simple_map_builder import SimpleMapBuilder
from map_builders.bsp_map_builder import BspMapBuilder
from map_builders.bps_interior_map_builder import BspInteriorMapBuilder
from map_builders.cellular_automata_builder import CellularAutomataBuilder
from map_builders.drunkard_builder import DrunkardsWalkBuilder
from map_builders.builder_structs import DrunkSpawnMode


def random_builder(depth):
    rand = randint(0, 6)
    if rand == 0:
        return BspInteriorMapBuilder(depth)
    elif rand == 1:
        return SimpleMapBuilder(depth)
    elif rand == 2:
        return BspMapBuilder(depth)
    elif rand == 3:
        return CellularAutomataBuilder(depth)
    elif rand == 4:
        return DrunkardsWalkBuilder(depth).open_area()
    elif rand == 5:
        return DrunkardsWalkBuilder(depth).open_halls()
    elif rand == 6:
        return DrunkardsWalkBuilder(depth).winding_passages()
    else:
        return SimpleMapBuilder(depth)


def build_random_map(depth):
    map_builder = random_builder(depth)
    map_builder.build_map()
    return map_builder

