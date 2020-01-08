import tcod as tcod

from copy import deepcopy

from systems.system import System
from world import World
from components.position_component import PositionComponent
from components.viewshed_component import ViewshedComponent
from components.hidden_component import HiddenComponent
from components.skills_component import Skills
from components.blocktile_component import BlockVisibilityComponent
from texts import Texts
from ui_system.render_functions import get_obfuscate_name
from player_systems.game_system import skill_roll_against_difficulty
import config


class VisibilitySystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(PositionComponent, ViewshedComponent)
        current_map = World.fetch('current_map')
        player = World.fetch('player')

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
            if entity == player:
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
            if entity == player:
                """ On n efface pas la current_map.visible_tiles.
                On regarde la nouvelle visible_tiles du viewshed du joueur.
                Si True dans viewshed: 
                    - si deja true dans current_amp, on ne change rien.
                    - si False dans current_map : on "decouvre" la tuile: on enregistre les entités.
                Si False dans viewshed:
                    - current_map : la tuile devient False."""
                # current_map.visible_tiles = [False] * (current_map.height * current_map.width)

                y = 0
                for row in viewshed.visible_tiles:
                    x = 0
                    for tile in row:
                        idx = current_map.xy_idx(x, y)
                        if not tile:
                            # player ne voit pas / plus cette tuile.
                            current_map.visible_tiles[idx] = False
                        else:
                            # Player see this tile.
                            if not current_map.visible_tiles[idx]:
                                # This tile couldnt be seen before. Return list
                                things_discovered.extend(player_see_tile(idx, current_map, player))
                            current_map.visible_tiles[idx] = True
                            current_map.revealed_tiles[idx] = True
                        x += 1
                    y += 1

            for entity_found in things_discovered:
                entity_found_name = get_obfuscate_name(entity_found)
                logs.appendleft(
                    f'[color={config.COLOR_MAJOR_INFO}]'
                    f'{Texts.get_text("YOU_SEE_")}' + f'{Texts.get_text(entity_found_name)}'
                    f'[/color]')


def player_see_tile(idx, current_map, player):
    """This tile was visible False before, and now is visible True.
    The player may know this tile from before, but wasnt saw its content one round before.
    return list of all entities in the tile if any."""
    entities_in_tile = list()
    # reveal hidden things in tile
    for entity in current_map.tile_content[idx]:
        # if hidden, roll has to be made to see it.
        maybe_hidden = World.get_entity_component(entity, HiddenComponent)
        if maybe_hidden:
            hidden_entity_seen = player_try_to_see_hidden_entity(player, entity)
            if hidden_entity_seen:
                entities_in_tile.append(entity)
        else:
            entities_in_tile.append(entity)
    return entities_in_tile


def player_try_to_see_hidden_entity(player, entity):
    # only trap for now
    if skill_roll_against_difficulty(player,
                                     Skills.FOUND_TRAPS,
                                     config.DEFAULT_TRAP_DETECTION_DIFFICULTY):
        # found it!
        World.remove_component(HiddenComponent, entity)
        return entity
