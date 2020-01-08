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
from map_builders.room_exploder import RoomExploder
from map_builders.room_corner_rounding import RoomCornerRounding
from map_builders.rooms_corridors_dogleg import DogLegCorridors
from map_builders.bsp_corridors import BSPCorridors
from map_builders.room_sorter import RoomSorter
from map_builders.builder_structs import StartX, StartY, RoomSort
from map_builders.room_drawer import RoomDrawer
from map_builders.nearest_room_corridors import NearestCorridor
from map_builders.room_corridor_lines import CorridorLines
from map_builders.room_corridor_spawner import CorridorSpawner
from map_builders.door_placement import DoorPlacement
from map_builders.diagonal_tile_path_cleaner import DiagonalTilePathCleaner

from map_builders.cellular_automata_builder import CellularAutomataBuilder
from map_builders.drunkard_builder import DrunkardsWalkBuilder
from map_builders.maze_builder import MazeBuilder
from map_builders.diffusion_limited_aggregation_builder import DLABuilder
from map_builders.prefab_builder import PrefabBuilder, PrefabSection, PrefabRoom, PrefabLevel
from map_builders.builder_structs import RIGHT_FORT, TOTALY_NOT_A_TRAP, \
    VerticalPlacement, HorizontalPlacement, LEVEL_MAP

from ui_system.interface import Interface


def random_build_example(depth):
    rand = randint(0, 19)
    if rand == 0:
        builder = BuilderChain(depth)
        builder.start_with(SimpleMapBuilder())
        builder.build_with(DogLegCorridors())
        builder.build_with(RoomBasedSpawner())
        builder.build_with(RoomBasedStartingPosition())
        builder.build_with(RoomBasedStairs())
        return builder
    elif rand == 1:
        builder = BuilderChain(depth)
        builder.start_with(BspMapBuilder())
        builder.build_with(RoomSorter(RoomSort.CENTRAL))
        builder.build_with(BSPCorridors())
        builder.build_with(RoomBasedSpawner())
        builder.build_with(RoomBasedStartingPosition())
        builder.build_with(RoomBasedStairs())
        return builder
    elif rand == 2:
        builder = BuilderChain(depth)
        builder.start_with(BspInteriorMapBuilder())
        builder.build_with(BSPCorridors())
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
    if rand == 15:
        builder = BuilderChain(depth)
        builder.start_with(DLABuilder().walk_outwards())
        builder.build_with(CellularAutomataBuilder())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 16:
        builder = BuilderChain(depth)
        builder.start_with(SimpleMapBuilder())
        builder.build_with(DogLegCorridors())
        builder.build_with(DrunkardsWalkBuilder().winding_passages())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 17:
        builder = BuilderChain(depth)
        builder.start_with(SimpleMapBuilder())
        builder.build_with(DogLegCorridors())
        builder.build_with(DLABuilder().heavy_erosion())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 18:    # très sympa
        builder = BuilderChain(depth)
        builder.start_with(BspMapBuilder())
        builder.build_with(RoomSorter(RoomSort.LEFTMOST))
        builder.build_with(BSPCorridors())
        builder.build_with(RoomExploder())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder
    elif rand == 19:
        builder = BuilderChain(depth)
        builder.start_with(BspMapBuilder())
        builder.build_with(RoomSorter(RoomSort.LEFTMOST))
        builder.build_with(BSPCorridors())
        builder.build_with(RoomCornerRounding())
        builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
        builder.build_with(CullUnreachable())
        builder.build_with(VoronoiSpawning())
        builder.build_with(DistantExit())
        return builder


def random_room_builder(builder):
    build_rand = randint(1, 3)
    print(f'build rand is {build_rand}')
    if build_rand == 1:
        builder.start_with(SimpleMapBuilder())
    elif build_rand == 2:
        builder.start_with(BspMapBuilder())
    elif build_rand == 3:
        builder.start_with(BspInteriorMapBuilder())

    if build_rand != 3:
        sort_roll = randint(0, 5)
        print(f'sort roll is {sort_roll} and build rand {build_rand} cant be 3')
        if sort_roll == 0:
            builder.build_with(RoomSorter(RoomSort.NONE))
        elif sort_roll == 1:
            builder.build_with(RoomSorter(RoomSort.LEFTMOST))
        elif sort_roll == 2:
            builder.build_with(RoomSorter(RoomSort.RIGHTMOST))
        elif sort_roll == 3:
            builder.build_with(RoomSorter(RoomSort.BOTTOMMOST))
        elif sort_roll == 4:
            builder.build_with(RoomSorter(RoomSort.TOPMOST))
        elif sort_roll == 5:
            builder.build_with(RoomSorter(RoomSort.CENTRAL))

    builder.build_with(RoomDrawer())

    corridor_roll = randint(1, 4)
    print(f'corridor rand is {corridor_roll}')
    if corridor_roll == 1:
        builder.build_with(DogLegCorridors())
    elif corridor_roll == 2:
        builder.build_with(BSPCorridors())
    elif corridor_roll == 3:
        builder.build_with(NearestCorridor())
    elif corridor_roll == 4:
        builder.build_with(CorridorLines())

    modifier_roll = randint(1, 3)
    print(f'modifier roll is {modifier_roll}')
    if modifier_roll == 1:
        builder.build_with(RoomExploder())
    elif modifier_roll == 2:
        builder.build_with(RoomCornerRounding())
    else:
        print(f'no modification')

    start_roll = randint(1, 2)
    print(f'room: start roll is {start_roll}')
    if start_roll == 1:
        builder.build_with(RoomBasedStartingPosition())
    elif start_roll == 2:
        start_x, start_y = random_start_position()
        builder.build_with(AreaStartingPosition(start_x, start_y))

    exit_roll = randint(1, 2)
    print(f'exit roll is {exit_roll}')
    if exit_roll == 1:
        builder.build_with(RoomBasedStairs())
    elif exit_roll == 2:
        builder.build_with(DistantExit())

    spawn_roll = randint(1, 3)
    print(f'spawn roll is {spawn_roll}')
    if spawn_roll == 1:
        builder.build_with(RoomBasedSpawner())
    elif spawn_roll == 2:
        builder.build_with(VoronoiSpawning())
    elif spawn_roll == 3:
        builder.build_with(CorridorSpawner())


def random_shape_builder(builder):
    builder_roll = randint(1, 12)
    print(f'random shape : builder roll is {builder_roll}')
    if builder_roll == 1:
        builder.start_with(CellularAutomataBuilder())
    elif builder_roll == 2:
        builder.start_with(DrunkardsWalkBuilder().open_area())
    elif builder_roll == 3:
        builder.start_with(DrunkardsWalkBuilder().open_halls())
    elif builder_roll == 4:
        builder.start_with(DrunkardsWalkBuilder().winding_passages())
    elif builder_roll == 5:
        builder.start_with(DrunkardsWalkBuilder().fat_passages())
    elif builder_roll == 6:
        builder.start_with(DrunkardsWalkBuilder().fearfull_symmetry())
    elif builder_roll == 7:
        builder.start_with(MazeBuilder())
    elif builder_roll == 8:
        builder.start_with(DLABuilder().walk_inwards())
    elif builder_roll == 9:
        builder.start_with(DLABuilder().walk_outwards())
    elif builder_roll == 10:
        builder.start_with(DLABuilder().central_attractor())
    elif builder_roll == 11:
        builder.start_with(DLABuilder().insectoid())
    elif builder_roll == 12:
        builder.start_with(PrefabBuilder(PrefabLevel(LEVEL_MAP, 80, 42)))

    builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
    builder.build_with(CullUnreachable())

    start_x, start_y = random_start_position()
    builder.build_with(AreaStartingPosition(start_x, start_y))

    builder.build_with(VoronoiSpawning())
    builder.build_with(DistantExit())


def random_builder(depth, width, height):
    builder = BuilderChain(depth, width, height)
    type_roll = randint(1, 2)
    print(f'random builder : type is {type_roll}')
    if type_roll == 1:
        random_room_builder(builder)
    elif type_roll == 2:
        random_shape_builder(builder)

    prefab_rand = randint(1, 20)
    print(f'prefab_rand is {prefab_rand}')
    if prefab_rand == 1:
        builder.build_with(PrefabBuilder(
            PrefabSection(RIGHT_FORT, 15, 43, (HorizontalPlacement.RIGHT, VerticalPlacement.TOP))))

    builder.build_with(DiagonalTilePathCleaner())
    builder.build_with(DoorPlacement())
    builder.build_with(PrefabBuilder(PrefabRoom('', 1, 1, 1, 100))) # TO FIX

    return builder


def random_start_position():
    result_x, result_y = None, None

    roll_x = randint(1, 3)
    if roll_x == 1:
        result_x = StartX.LEFT
    elif roll_x == 2:
        result_x = StartX.CENTER
    elif roll_x == 3:
        result_x = StartX.RIGHT

    roll_y = randint(1, 3)
    if roll_y == 1:
        result_y = StartY.TOP
    elif roll_y == 2:
        result_y = StartY.CENTER
    elif roll_y == 3:
        result_y = StartY.BOTTOM

    return result_x, result_y


def build_random_map(depth, width, height):
    Interface.map_screen_width = width
    Interface.map_screen_height = height
    Interface.set_zoom(Interface.zoom)

    # return random_build_example(depth)
    # return random_builder(depth, width, height)

    '''
    builder = BuilderChain(depth, width, height)
    builder.start_with(SimpleMapBuilder())
    builder.build_with(RoomDrawer())
    builder.build_with(RoomCornerRounding())
    builder.build_with(RoomSorter(RoomSort.LEFTMOST))
    builder.build_with(RoomExploder())
    builder.build_with(NearestCorridor())
    builder.build_with(DoorPlacement())
    builder.build_with(CorridorSpawner())
    builder.build_with(RoomBasedStairs())
    builder.build_with(RoomBasedStartingPosition())
    builder.build_with(PrefabBuilder(PrefabRoom(None, 1, 1, 1, 100)))
    return builder
    '''

    builder = BuilderChain(depth, width, height)
    builder.start_with(DLABuilder().insectoid())
    builder.build_with(AreaStartingPosition(StartX.CENTER, StartY.CENTER))
    builder.build_with(CullUnreachable())
    builder.build_with(DiagonalTilePathCleaner())
    builder.build_with(VoronoiSpawning())
    builder.build_with(DistantExit())
    return builder

