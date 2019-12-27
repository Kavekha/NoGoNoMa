from random import randint

from map_builders.builder_map import BuilderChain
from map_builders.simple_map_builder import SimpleMapBuilder
from map_builders.room_based_spawner import RoomBasedSpawner
from map_builders.room_based_stairs import RoomBasedStairs
from map_builders.room_based_starting_position import RoomBasedStartingPosition
from map_builders.bsp_map_builder import BspMapBuilder
from map_builders.bps_interior_map_builder import BspInteriorMapBuilder
from map_builders.area_starting_position import AreaStartingPosition
from map_builders.cull_unreachable import CullUnreachable
from map_builders.voronoi_spawning import VoronoiSpawning
from map_builders.distant_exit import DistantExit
from gmap.gmap_enums import StartX, StartY


from map_builders.cellular_automata_builder import CellularAutomataBuilder
from map_builders.drunkard_builder import DrunkardsWalkBuilder
from map_builders.maze_builder import MazeBuilder
from map_builders.diffusion_limited_aggregation_builder import DLABuilder
from map_builders.prefab_builder import PrefabBuilder, PrefabSection, PrefabRoom
from map_builders.builder_structs import RIGHT_FORT, TOTALY_NOT_A_TRAP, \
    VerticalPlacement, HorizontalPlacement


def old_random_builder(depth):
    rand = randint(0, 13)
    if rand == 0:
        result = BspInteriorMapBuilder(depth)
    elif rand == 1:
        result = SimpleMapBuilder() # (depth)
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
        result = SimpleMapBuilder()     # (depth)

    if randint(1, 3) == 1:
        result = PrefabBuilder(depth,
                      PrefabSection(RIGHT_FORT, 15, 43, (HorizontalPlacement.RIGHT, VerticalPlacement.TOP)),
                      result)

    result = PrefabBuilder(depth,
                           PrefabRoom(TOTALY_NOT_A_TRAP, 5, 5, 0, 100),
                           result)

    return result


def random_build(depth):
    rand = 3   # randint(0, 2)
    if rand == 0:
        builder = BuilderChain(depth)
        builder.start_with(SimpleMapBuilder())
        builder.build_with(RoomBasedSpawner())
        builder.build_with(RoomBasedStartingPosition())
        builder.build_with(RoomBasedStairs())
        return builder
    elif rand == 1:
        builder = BuilderChain(depth)
        builder.start_with(BspMapBuilder())
        builder.build_with(RoomBasedSpawner())
        builder.build_with(RoomBasedStartingPosition())
        builder.build_with(RoomBasedStairs())
        return builder
    elif rand == 2:
        builder = BuilderChain(depth)
        builder.start_with(BspInteriorMapBuilder())
        builder.build_with(RoomBasedSpawner())
        builder.build_with(RoomBasedStartingPosition())
        builder.build_with(RoomBasedStairs())
        return builder
    elif rand == 3:
        builder = BuilderChain(depth)
        builder.start_with(CellularAutomataBuilder())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder


def build_random_map(depth):
    return random_build(depth)


