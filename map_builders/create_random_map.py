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


def random_build(depth):
    rand = randint(0, 14)
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
    elif rand == 4:
        builder = BuilderChain(depth)
        builder.start_with(DrunkardsWalkBuilder().open_area())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 5:
        builder = BuilderChain(depth)
        builder.start_with(DrunkardsWalkBuilder().open_halls())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 6:
        builder = BuilderChain(depth)
        builder.start_with(DrunkardsWalkBuilder().winding_passages())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 7:
        builder = BuilderChain(depth)
        builder.start_with(DrunkardsWalkBuilder().fat_passages())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 8:
        builder = BuilderChain(depth)
        builder.start_with(DrunkardsWalkBuilder().fearfull_symmetry())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 9:
        builder = BuilderChain(depth)
        builder.start_with(DLABuilder().walk_inwards())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 10:    # Not interresting at all
        builder = BuilderChain(depth)
        builder.start_with(DLABuilder().walk_outwards())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 11:
        builder = BuilderChain(depth)
        builder.start_with(DLABuilder().central_attractor())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 12:
        builder = BuilderChain(depth)
        builder.start_with(DLABuilder().insectoid())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 13:
        builder = BuilderChain(depth)
        builder.start_with(MazeBuilder())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 14:
        builder = BuilderChain(depth)
        builder.start_with(CellularAutomataBuilder())
        builder.build_with(PrefabBuilder(PrefabRoom(TOTALY_NOT_A_TRAP, 5, 5, 0, 100)))
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(PrefabBuilder(
            PrefabSection(RIGHT_FORT, 15, 43, (HorizontalPlacement.RIGHT, VerticalPlacement.TOP)))
        )
        builder.build_with(DistantExit())
        return builder


def build_random_map(depth):
    return random_build(depth)


