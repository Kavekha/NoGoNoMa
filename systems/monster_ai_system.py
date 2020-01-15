import tcod as tcod

import math

from systems.system import System
from components.character_components import MonsterComponent
from components.viewshed_component import ViewshedComponent
from components.position_components import PositionComponent
from components.name_components import NameComponent
from components.intent_components import WantsToMeleeComponent
from components.status_effect_components import ConfusionComponent
from components.initiative_components import MyTurn
from systems.particule_system import ParticuleBuilder
from player_systems.try_move_player import move_to, action_wait
from map_builders.commons import distance_to
from world import World


class MonsterAi(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(NameComponent, MonsterComponent, ViewshedComponent, PositionComponent, MyTurn)

        player = World.fetch('player')
        player_position = World.get_entity_component(player, PositionComponent)
        x, y = player_position.x, player_position.y

        for entity, (name, monster, viewshed, position_component, _myturn, *args) in subjects:
            can_act = True
            is_confused = World.get_entity_component(entity, ConfusionComponent)
            if is_confused:
                is_confused.turns -= 1
                if is_confused.turns < 1:
                    World.remove_component(ConfusionComponent, entity)
                can_act = False
                ParticuleBuilder.request(position_component.x,
                                         position_component.y, 'magenta', '?', 'particules/confusion.png')

            if can_act:
                print(f'monster ai: player position is {player_position.x, player_position.y} - checking {x, y}')
                if viewshed.visible_tiles[y][x]:
                    print(f'me, monster {entity}, I see player position')
                    if distance_to(position_component.x, position_component.y,
                                   player_position.x, player_position.y) <= 1.5:
                        want_to_melee = WantsToMeleeComponent(player)
                        World.add_component(want_to_melee, entity)
                    else:
                        move_astar = self.move_astar(entity, viewshed, position_component, player_position.x, player_position.y)
                        current_map = World.fetch('current_map')
                        if move_astar:
                            x, y = move_astar
                            move_to(x, y, entity, current_map)
                        else:
                            print(f'astar didnt work. Move towards instead.')
                            self.move_towards(entity, position_component, player_position.x, player_position.y, current_map)
                else:
                    print(f'me, monster {entity}, I dont see player and wait. Im at {position_component.x, position_component.y}')
                    # do nothing, pass its turn.
                    action_wait(entity)

    def move_towards(self, entity, position_component, target_x, target_y, current_map):
        current_map = World.fetch('current_map')
        dx = target_x - position_component.x
        dy = target_y - position_component.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if dx != 0:
            dx = int(round(dx // distance))
        if dy != 0:
            dy = int(round(dy // distance))

        new_pos_x = min(current_map.width - 1, max(0, position_component.x + dx))
        new_pos_y = min(current_map.height - 1, max(0, position_component.y + dy))

        move_to(new_pos_x, new_pos_y, entity, current_map)

    def move_astar(self, entity, viewshed, position_component, player_x, player_y):  # target, entities, game_map):
        # /!\ On utilise visible_tiles, qui concerne ce que le mob voit = le transparent est consideré comme walkable.
        # /!\ Libtcod fonctionne en y,x et pas en x, y. Melange facile à faire, a ameliorer!
        # /!\ Pas de second check sur le deplacement, on teleporte le mob. Danger si walkable.
        # Create a FOV map that has the dimensions of the map
        fov = viewshed.visible_tiles
        current_map = World.fetch('current_map')

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        tcod.path_compute(my_path, position_component.y, position_component.x, player_y, player_x)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths
        # (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map
        # if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            y, x = tcod.path_walk(my_path, True)  # tcod : [y][x]
            if x or y:
                tcod.path_delete(my_path)
                return x, y
                # Set self's coordinates to the next path tile
        tcod.path_delete(my_path)
        return False
