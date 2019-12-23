from world import World
import config
from components.position_component import PositionComponent
from components.player_component import PlayerComponent
from components.viewshed_component import ViewshedComponent
from components.pools_component import Pools
from components.wants_to_melee_component import WantsToMeleeComponent
from components.triggers_components import EntityMovedComponent
from gmap.utils import xy_idx
from gmap.gmap_enums import TileType
from ui_system.ui_enums import NextLevelResult
from texts import Texts


def try_move_player(delta_x, delta_y):
    subjects = World.get_components(PositionComponent, PlayerComponent)
    if not subjects:
        return

    current_map = World.fetch('current_map')
    for entity, (position, player) in subjects:
        destination_idx = xy_idx(position.x + delta_x, position.y + delta_y)

        for potential_target in current_map.tile_content[destination_idx]:
            target = World.get_entity_component(potential_target, Pools)
            if target:
                want_to_melee = WantsToMeleeComponent(potential_target)
                World.add_component(want_to_melee, entity)
                return

        if not current_map.blocked_tiles[destination_idx]:
            position.x = min(config.MAP_WIDTH -1, max(0, position.x + delta_x))
            position.y = min(config.MAP_HEIGHT -1, max(0, position.y + delta_y))
            player_viewshed = World.get_entity_component(entity, ViewshedComponent)
            player_viewshed.dirty = True
            has_moved = EntityMovedComponent()
            World.add_component(has_moved, entity)


def try_next_level():
    player_pos = World.get_entity_component(World.fetch('player'), PositionComponent)
    logs = World.fetch('logs')
    current_map = World.fetch('current_map')
    if current_map.tiles[xy_idx(player_pos.x, player_pos.y)] == TileType.DOWN_STAIRS:
        return NextLevelResult.NEXT_FLOOR
    elif current_map.tiles[xy_idx(player_pos.x, player_pos.y)] == TileType.EXIT_PORTAL:
        return NextLevelResult.EXIT_DUNGEON
    logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]{Texts.get_text("NO_WAY_DOWN")}[/color]')
    return NextLevelResult.NO_EXIT
