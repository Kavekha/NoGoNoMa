from systems.system import System
from world import World

from components.position_components import PositionComponent
from components.item_components import InBackPackComponent
from components.intent_components import WantsToDropComponent
from texts import Texts
from ui_system.render_functions import get_obfuscate_name
import config


class ItemDropSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToDropComponent)
        if not subjects:
            return

        player = World.fetch('player')
        logs = World.fetch('logs')
        for entity, (wants_to_drop, *args) in subjects:
            entity_position = World.get_entity_component(entity, PositionComponent)
            drop_position = PositionComponent(entity_position.x, entity_position.y)
            World.add_component(drop_position, wants_to_drop.item)
            World.remove_component(InBackPackComponent, wants_to_drop.item)

            if entity == player:
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]{Texts.get_text("YOU_DROP_UP")}'
                                f'{get_obfuscate_name(wants_to_drop.item)}[/color]')

            World.remove_component(WantsToDropComponent, entity)
