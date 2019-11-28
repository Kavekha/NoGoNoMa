from world import World
import config
from components.position_component import PositionComponent
from components.player_component import PlayerComponent
from components.viewshed_component import ViewshedComponent
from components.combat_stats_component import CombatStatsComponent
from components.wants_to_melee_component import WantsToMeleeComponent
from gmap.utils import xy_idx
from data.types import TileType


def try_move_player(delta_x, delta_y):
    subjects = World.get_components(PositionComponent, PlayerComponent)
    if not subjects:
        return

    current_map = World.fetch('current_map')
    for entity, (position, player) in subjects:
        destination_idx = current_map.xy_idx(position.x + delta_x, position.y + delta_y)

        for potential_target in current_map.tile_content[destination_idx]:
            target = World.get_entity_component(potential_target, CombatStatsComponent)
            if target:
                print(f'Player attack!')
                want_to_melee = WantsToMeleeComponent(potential_target)
                World.add_component(want_to_melee, entity)
                return

        if not current_map.blocked_tiles[destination_idx]:
            position.x = min(config.MAP_WIDTH -1, max(0, position.x + delta_x))
            position.y = min(config.MAP_HEIGHT -1, max(0, position.y + delta_y))
            World.insert('player_pos', (position.x, position.y))
            player_viewshed = World.get_entity_component(entity, ViewshedComponent)
            player_viewshed.dirty = True


def try_next_level():
    player_pos = World.get_entity_component(World.fetch('player'), PositionComponent)
    logs = World.fetch('logs')
    current_map = World.fetch('current_map')
    if current_map.tiles[xy_idx(player_pos.x, player_pos.y)] == TileType.DOWN_STAIRS:
        return True
    logs.appendleft(f"[color={config.COLOR_MAJOR_INFO}]There is no way down from here.[/color]")
    return False
