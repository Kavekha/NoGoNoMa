import tcod as tcod

import math

from systems.system import System
from components.monster_component import MonsterComponent
from components.viewshed_component import ViewshedComponent
from components.position_component import PositionComponent
from components.name_component import NameComponent
from components.wants_to_melee_component import WantsToMeleeComponent
from components.confusion_component import ConfusionComponent
from systems.particule_system import ParticuleBuilder
from state import States
from gmap.utils import distance_to
from world import World
import config


class MonsterAi(System):
    def update(self, *args, **kwargs):
        run_state = World.fetch('state')
        if not run_state.current_state == States.MONSTER_TURN:
            print(f'not monster turn')
            return
        print(f'monster turn!')

        subjects = World.get_components(NameComponent, MonsterComponent, ViewshedComponent, PositionComponent)

        player = World.fetch('player')
        player_position = World.get_entity_component(player, PositionComponent)
        x, y = player_position.x, player_position.y

        for entity, (name, monster, viewshed, position_component, *args) in subjects:
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
                if viewshed.visible_tiles[y][x]:
                    if distance_to(position_component.x, position_component.y,
                                   player_position.x, player_position.y) <= 1:
                        want_to_melee = WantsToMeleeComponent(player)
                        World.add_component(want_to_melee, entity)
                    else:
                        self.move_astar(viewshed, position_component, player_position.x, player_position.y)
            else:
                print(f'{name.name} is confused.')

    def move_towards(self, position_component, target_x, target_y):
        dx = target_x - position_component.x
        dy = target_y - position_component.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if dx != 0:
            dx = int(round(dx // distance))
        if dy != 0:
            dy = int(round(dy // distance))

        current_map = World.fetch('current_map')
        new_pos_x = min(config.MAP_WIDTH - 1, max(0, position_component.x + dx))
        new_pos_y = min(config.MAP_HEIGHT - 1, max(0, position_component.y + dy))
        if not current_map.blocked_tiles[current_map.xy_idx(new_pos_x, new_pos_y)]:
            position_component.x = new_pos_x
            position_component.y = new_pos_y

    def move_astar(self, viewshed, position_component, player_x, player_y): #target, entities, game_map):
        # /!\ On utilise visible_tiles, qui concerne ce que le mob voit = le transparent est consideré comme walkable.
        # /!\ Libtcod fonctionne en y,x et pas en x, y. Melange facile à faire, a ameliorer!
        # /!\ Pas de second check sur le deplacement, on teleporte le mob. Danger si walkable.
        # Create a FOV map that has the dimensions of the map
        fov = viewshed.visible_tiles

        '''
        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(config.MAP_HEIGHT):
            for x1 in range(config.MAP_WIDTH):
                # print(f'a star blocked tiles : {current_map.blocked_tiles}')
                libtcod.map_set_properties(fov, x1, y1, True,
                                           not current_map.blocked_tiles[xy_idx(x1, y1)])
        '''
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
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                position_component.x = y
                position_component.y = x
        else:
            # Keep the old move function as a backup so that if there are no paths
            # (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            print(f'astar didnt work. Move towards instead.')
            self.move_towards(position_component, player_x, player_y)

            # Delete the path to free memory
        tcod.path_delete(my_path)