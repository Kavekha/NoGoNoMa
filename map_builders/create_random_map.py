from random import randint

from map_builders.simple_map_builder import SimpleMapBuilder
from map_builders.bsp_map_builder import BspMapBuilder
from map_builders.bps_interior_map_builder import BspInteriorMapBuilder
from map_builders.cellular_automata_builder import CellularAutomataBuilder
from map_builders.drunkard_builder import DrunkardsWalkBuilder
from map_builders.maze_builder import MazeBuilder
from map_builders.diffusion_limited_aggregation_builder import DLABuilder
from map_builders.prefab_builder import PrefabBuilder, PrefabLevel, PrefabSection, PrefabRoom
from map_builders.builder_structs import LEVEL_MAP, RIGHT_FORT, TOTALY_NOT_A_TRAP, \
    VerticalPlacement, HorizontalPlacement


def random_builder(depth):
    rand = randint(0, 13)
    if rand == 0:
        result = BspInteriorMapBuilder(depth)
    elif rand == 1:
        result = SimpleMapBuilder(depth)
    elif rand == 2:
        result = BspMapBuilder(depth)
    elif rand == 3:
        result = CellularAutomataBuilder(depth)
    elif rand == 4:
        result = DrunkardsWalkBuilder(depth).open_area()
    elif rand == 5:
        result = DrunkardsWalkBuilder(depth).open_halls()
    elif rand == 6:
        result = DrunkardsWalkBuilder(depth).winding_passages()
    elif rand == 7:
        result = MazeBuilder(depth)
    elif rand == 8:
        result = DLABuilder(depth).walk_inwards()
    elif rand == 9:
        result = DLABuilder(depth).walk_outwards()
    elif rand == 10:
        result = DLABuilder(depth).central_attractor()
    elif rand == 11:
        result = DLABuilder(depth).insectoid()
    elif rand == 12:
        result = DrunkardsWalkBuilder(depth).fat_passages()
    elif rand == 13:
        result = DrunkardsWalkBuilder(depth).fearfull_symmetry()
    else:
        result = SimpleMapBuilder(depth)

    if randint(1, 3) == 1:
        result = PrefabBuilder(depth,
                      PrefabSection(RIGHT_FORT, 15, 43, (HorizontalPlacement.RIGHT, VerticalPlacement.TOP)),
                      result)

    result = PrefabBuilder(depth,
                           PrefabRoom(TOTALY_NOT_A_TRAP, 5, 5, 0, 100),
                           result)

    return result


def old_random_builder(depth):
    rand = 150 #randint(0, 13)
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
    elif rand == 8:
        return DLABuilder(depth).walk_inwards()
    elif rand == 9:
        return DLABuilder(depth).walk_outwards()
    elif rand == 10:
        return DLABuilder(depth).central_attractor()
    elif rand == 11:
        return DLABuilder(depth).insectoid()
    elif rand == 12:
        return DrunkardsWalkBuilder(depth).fat_passages()
    elif rand == 13:
        return DrunkardsWalkBuilder(depth).fearfull_symmetry()
    elif rand == 14:
        return PrefabBuilder(depth, PrefabLevel(LEVEL_MAP, 80, 42))
    elif rand == 15:
        return PrefabBuilder(depth,
                             PrefabSection(RIGHT_FORT, 15, 43, (HorizontalPlacement.RIGHT, VerticalPlacement.TOP)),
                             CellularAutomataBuilder(depth))
    elif rand == 16:
        return PrefabBuilder(depth,
                             PrefabRoom(TOTALY_NOT_A_TRAP, 5, 5, 0, 100),
                             SimpleMapBuilder(depth))
    else:
        return PrefabBuilder(depth,
                             PrefabRoom(TOTALY_NOT_A_TRAP, 5, 5, 0, 100),
                             SimpleMapBuilder(depth))


def build_random_map(depth):
    map_builder = random_builder(depth)
    map_builder.build_map()
    return map_builder

