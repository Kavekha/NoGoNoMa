from world import World
from map_builders.create_random_map import build_random_map
from components.position_component import PositionComponent
from components.viewshed_component import ViewshedComponent


def level_transition(new_depth):
    master_dungeon = World.fetch('master_dungeon')
    if master_dungeon.get_map(new_depth):
        return transition_to_existing_map(new_depth)
    else:
        return transition_to_new_map(new_depth)


def transition_to_new_map(new_depth):
    builder = build_random_map(new_depth, 80, 50)
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
    return map_gen_history


def transition_to_existing_map(new_depth):
    print(f'Backtracking not implemented')
    raise NotImplementedError
