from random import randint

from map_builders.simple_map_builder import SimpleMapBuilder
from map_builders.bsp_map_builder import BspMapBuilder
from map_builders.bps_interior_map_builder import BspInteriorMapBuilder
from map_builders.cellular_automata_builder import CellularAutomataBuilder
from map_builders.drunkard_builder import DrunkardsWalkBuilder
from map_builders.maze_builder import MazeBuilder


def random_builder(depth):
    rand = 10   #randint(0, 7)
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
    elif rand == 7:
        return MazeBuilder(depth)
    else:
        return MazeBuilder(depth)


def build_random_map(depth):
    map_builder = random_builder(depth)
    map_builder.build_map()
    return map_builder

