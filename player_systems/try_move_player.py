from world import World
import config
from components.position_components import PositionComponent, EntityMovedComponent
from components.viewshed_component import ViewshedComponent
from components.character_components import AutopickupComponent
from components.blocktile_component import BlockTileComponent
from systems.inventory_system import get_item
from components.pools_component import Pools
from components.wants_to_melee_component import WantsToMeleeComponent
from components.door_component import DoorComponent
from player_systems.game_system import opening_door
from player_systems.initiative_costs_mecanisms import calculate_move_cost, wait_turn_cost
from gmap.gmap_enums import TileType
from ui_system.ui_enums import NextLevelResult
from texts import Texts


def can_move_on_tile(x, y):
    current_map = World.fetch('current_map')
    if not current_map.blocked_tiles[current_map.xy_idx(x, y)]:
        return True
    return False


def move_on_click_player(dx, dy):
    player = World.fetch('player')
    player_position = World.get_entity_component(player, PositionComponent)
    x, y = 0, 0
    if dx - player_position.x > 0:
        x += 1
    elif dx - player_position.x < 0:
        x -= 1
    if dy - player_position.y > 0:
        y += 1
    elif dy - player_position.y < 0:
        y -= 1
    try_move_player(x, y)


def available_tile_for_move(destination_idx):
    current_map = World.fetch('current_map')
    if not current_map.blocked_tiles[destination_idx] and not current_map.out_of_bound(destination_idx):
        return True
    return False


def try_move_player(delta_x, delta_y):
    print(f'MOVING!')
    player = World.fetch('player')
    player_pos = World.get_entity_component(player, PositionComponent)

    # anti auto kill si clic sur soit meme avec move by click
    if not delta_x and not delta_y:
        return

    current_map = World.fetch('current_map')
    destination_idx = current_map.xy_idx(player_pos.x + delta_x, player_pos.y + delta_y)

    for potential_target in current_map.tile_content[destination_idx]:
        target = World.get_entity_component(potential_target, Pools)
        if target:
            want_to_melee = WantsToMeleeComponent(potential_target)
            World.add_component(want_to_melee, player)
            return
        door = World.get_entity_component(potential_target, DoorComponent)
        if door:
            opening_door(potential_target, door)

    x, y = current_map.index_to_point2d(destination_idx)
    move_to(x, y, player, current_map)


def move_to(x, y, entity, current_map):
    entity_pos = World.get_entity_component(entity, PositionComponent)
    from_idx = current_map.xy_idx(entity_pos.x, entity_pos.y)
    idx = current_map.xy_idx(x, y)

    # if not current_map.blocked_tiles[destination_idx] and not current_map.out_of_bound(destination_idx):
    if available_tile_for_move(idx):
        entity_pos.x = x
        entity_pos.y = y
        if World.get_entity_component(entity, BlockTileComponent):
            current_map.blocked_tiles[from_idx] = False
            current_map.blocked_tiles[idx] = True

        viewshed = World.get_entity_component(entity, ViewshedComponent)
        if viewshed:
            viewshed.dirty = True

        # autopickup
        if World.get_entity_component(entity, AutopickupComponent):
            get_item(entity)

        World.add_component(EntityMovedComponent(), entity)
        World.add_component(calculate_move_cost(entity), entity)


def action_wait(entity):
    World.add_component(wait_turn_cost(entity), entity)


def try_next_level():
    player_pos = World.get_entity_component(World.fetch('player'), PositionComponent)
    logs = World.fetch('logs')
    current_map = World.fetch('current_map')
    if current_map.tiles[current_map.xy_idx(player_pos.x, player_pos.y)] == TileType.DOWN_STAIRS:
        return NextLevelResult.NEXT_FLOOR
    elif current_map.tiles[current_map.xy_idx(player_pos.x, player_pos.y)] == TileType.EXIT_PORTAL:
        return NextLevelResult.EXIT_DUNGEON
    logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]{Texts.get_text("NO_WAY_DOWN")}[/color]')
    return NextLevelResult.NO_EXIT
