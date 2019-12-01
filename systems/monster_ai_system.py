import math

from systems.system import System
from components.monster_component import MonsterComponent
from components.viewshed_component import ViewshedComponent
from components.position_component import PositionComponent
from components.name_component import NameComponent
from components.wants_to_melee_component import WantsToMeleeComponent
from components.confusion_component import ConfusionComponent
from state import States
from gmap.utils import distance_to
from world import World
import config


class MonsterAi(System):
    def update(self, *args, **kwargs):
        run_state = World.fetch('state')
        if run_state.current_state != States.MONSTER_TURN:
            return

        subjects = World.get_components(NameComponent, MonsterComponent, ViewshedComponent, PositionComponent)
        if not subjects:
            return

        player = World.fetch('player')
        player_position = World.get_entity_component(player, PositionComponent)
        x, y = player_position.x, player_position.y

        for entity, (name, monster, viewshed, position, *args) in subjects:
            can_act = True
            is_confused = World.get_entity_component(entity, ConfusionComponent)
            if is_confused:
                is_confused.turns -= 1
                if is_confused.turns < 1:
                    World.remove_component(ConfusionComponent, entity)
                can_act = False

            if can_act:
                if viewshed.visible_tiles[y][x]:
                    if distance_to(position.x, position.y, player_position.x, player_position.y) <= 1:
                        want_to_melee = WantsToMeleeComponent(player)
                        World.add_component(want_to_melee, entity)
                    else:
                        self.move_towards(position, player_position.x, player_position.y)
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
