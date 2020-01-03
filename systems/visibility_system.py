import tcod as tcod

from copy import deepcopy

from systems.system import System
from world import World
from components.position_component import PositionComponent
from components.viewshed_component import ViewshedComponent
from components.player_component import PlayerComponent
from components.hidden_component import HiddenComponent
from components.skills_component import Skills
from components.blocktile_component import BlockVisibilityComponent
from components.name_component import NameComponent
from texts import Texts
from ui_system.render_functions import get_obfuscate_name
from player_systems.game_system import skill_roll_against_difficulty
import config


class VisibilitySystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(PositionComponent, ViewshedComponent)
        current_map = World.fetch('current_map')

        # fov map update needed if view blocked by something since last time.
        old_view_blocked = deepcopy(current_map.view_blocked)
        current_map.view_blocked.clear()
        for entity, (block_pos, _block) in World.get_components(PositionComponent, BlockVisibilityComponent):
            idx = current_map.xy_idx(block_pos.x, block_pos.y)
            current_map.view_blocked[idx] = True
        old_view_blocked = set(old_view_blocked.keys())
        new_view_blocked = set(deepcopy(current_map.view_blocked).keys())
        same_entries = new_view_blocked.intersection(old_view_blocked)
        if len(old_view_blocked) - len(same_entries) != len(new_view_blocked) - len(same_entries):
            # change in view blocked
            current_map.create_fov_map()

        # viewshed update.
        for entity, (position, viewshed) in subjects:
            viewshed.dirty = False
            viewshed.visible_tiles = []
            if entity == World.fetch('player'):
                # on enregistre les murs comme visibles
                current_map.fov_map.compute_fov(position.x, position.y, viewshed.visible_range,
                                                viewshed.light_wall, tcod.FOV_BASIC)
            else:
                current_map.fov_map.compute_fov(position.x, position.y, viewshed.visible_range,
                                                False, tcod.FOV_BASIC)
            viewshed.visible_tiles = current_map.fov_map.fov.copy()

            things_discovered = list()
            logs = World.fetch('logs')
            # visible map is Y X (fov map numpy tcod)
            if World.entity_has_component(entity, PlayerComponent):
                current_map.visible_tiles = [False] * (current_map.height * current_map.width)

                y = 0
                for row in viewshed.visible_tiles:
                    x = 0
                    for tile in row:
                        if tile:
                            idx = current_map.xy_idx(x, y)
                            # reveal hidden things in tile
                            for entity_tile_content in current_map.tile_content[idx]:
                                entity_name = World.get_entity_component(entity_tile_content, NameComponent)
                                if entity_name:
                                    entity_name = get_obfuscate_name(entity_tile_content)
                                    maybe_hidden = World.get_entity_component(entity_tile_content, HiddenComponent)
                                    if maybe_hidden:
                                        # roll found trap for detecting
                                        if skill_roll_against_difficulty(entity,
                                                                         Skills.FOUND_TRAPS,
                                                                         config.DEFAULT_TRAP_DETECTION_DIFFICULTY):
                                            # found it!
                                            World.remove_component(HiddenComponent, entity_tile_content)
                                            things_discovered.append(entity_name)
                                    else:
                                        # si cette tile est sur le point d'être dévoilée.
                                        if not current_map.revealed_tiles[idx]:
                                            things_discovered.append(entity_name)

                            # marked as visible & revealed
                            current_map.revealed_tiles[idx] = True
                            current_map.visible_tiles[idx] = True
                        x += 1
                    y += 1



            for entity_found in things_discovered:
                logs.appendleft(
                    f'[color={config.COLOR_MAJOR_INFO}]'
                    f'{Texts.get_text("YOU_SPOTTED_").format(Texts.get_text(entity_found))}'
                    f'[/color]')
