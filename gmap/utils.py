import math

import config
from world import World
from map_builders.create_random_map import build_random_map
from components.position_component import PositionComponent
from components.viewshed_component import ViewshedComponent


def distance_to(self_position_x, self_position_y, other_position_x, other_position_y):
    dx = other_position_x - self_position_x
    dy = other_position_y - self_position_y
    return math.sqrt(dx ** 2 + dy ** 2)


def index_to_point2d(idx):
    # Transform an idx 1D array to a x, y format for 2D array
    return int(idx % config.MAP_WIDTH), idx // config.MAP_WIDTH


def xy_idx(x, y):
    # Return the map tile (x, y). Avoid List in list [x][y]
    return (y * config.MAP_WIDTH) + x


def level_transition(new_depth):
    master_dungeon = World.fetch('master_dungeon')
    if master_dungeon.get_map(new_depth):
        return transition_to_existing_map(new_depth)
    else:
        return transition_to_new_map(new_depth)


def transition_to_new_map(new_depth):
    builder = build_random_map(new_depth)
    builder.build_map()

    current_map = builder.build_data.map
    World.insert('current_map', current_map)

    x, y = builder.build_data.starting_position
    player = World.fetch('player')
    player_pos = World.get_entity_component(player, PositionComponent)
    player_pos.x, player_pos.y = x, y
    player_viewshed = World.get_entity_component(player, ViewshedComponent)
    player_viewshed.dirty = True

    master_dungeon = World.fetch('master_dungeon')
    master_dungeon.store_map(new_depth, current_map)

    builder.spawn_entities()

    map_gen_history = builder.build_data.history
    return map_gen_history


def old_transition_to_new_map(new_depth):
    builder = build_random_map(new_depth)
    current_map = builder.get_map()
    World.insert('current_map', current_map)

    x, y = builder.get_starting_position()
    player = World.fetch('player')
    player_pos = World.get_entity_component(player, PositionComponent)
    player_pos.x, player_pos.y = x, y
    player_viewshed = World.get_entity_component(player, ViewshedComponent)
    player_viewshed.dirty = True

    master_dungeon = World.fetch('master_dungeon')
    master_dungeon.store_map(new_depth, current_map)

    map_gen_history = builder.get_snapshot_history()
    print(f'transition: map gen history is {map_gen_history}')
    print(f'transition : map gen history type is {type(map_gen_history)}')
    return map_gen_history


def transition_to_existing_map(new_depth):
    print(f'Backtracking not implemented')
    raise NotImplementedError

'''
    dungeon_master = World.fetch('dungeon_master')
    current_map = dungeon_master.get_map(new_depth)
    World.insert('current_map', current_map)

    # Reperer le Upstair et placer le joueur dessus.

    player = World.fetch('player')
    player_pos = World.get_entity_component(player, PositionComponent)
    player_pos.x, player_pos.y = x, y
    player_viewshed = World.get_entity_component(player, ViewshedComponent)
    player_viewshed.dirty = True
    '''