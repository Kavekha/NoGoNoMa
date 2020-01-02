from world import World
import config
from components.position_component import PositionComponent
from components.autopickup_component import AutopickupComponent
from components.viewshed_component import ViewshedComponent
from components.pools_component import Pools
from components.wants_to_melee_component import WantsToMeleeComponent
from components.triggers_components import EntityMovedComponent
from components.wants_to_pickup_component import WantsToPickUpComponent
from components.name_component import NameComponent
from components.door_component import DoorComponent
from player_systems.game_system import opening_door
from gmap.gmap_enums import TileType
from ui_system.ui_enums import NextLevelResult
from systems.inventory_system import get_item
from texts import Texts


def try_move_player(delta_x, delta_y):
    player = World.fetch('player')
    player_pos = World.get_entity_component(player, PositionComponent)

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

    if not current_map.blocked_tiles[destination_idx] and not current_map.out_of_bound(destination_idx):
        player_pos.x = min(current_map.width - 1, max(0, player_pos.x + delta_x))
        player_pos.y = min(current_map.height - 1, max(0, player_pos.y + delta_y))

        player_viewshed = World.get_entity_component(player, ViewshedComponent)
        player_viewshed.dirty = True

        has_moved = EntityMovedComponent()
        World.add_component(has_moved, player)

        if World.get_entity_component(player, AutopickupComponent):
            get_item(player)


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
