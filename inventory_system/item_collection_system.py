from world import World
from systems.system import System
from components.intent_components import WantsToPickUpComponent
from components.position_components import PositionComponent
from components.item_components import InBackPackComponent
from ui_system.render_functions import get_obfuscate_name
import config
from texts import Texts


class ItemCollectionSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToPickUpComponent)

        for entity, (wants_to_pickup, *args) in subjects:
            # remove position. Can be pickup already check before, when WantsToPickupComponent was put)
            World.remove_component(PositionComponent, wants_to_pickup.item)
            backpack = InBackPackComponent(entity)
            World.add_component(backpack, wants_to_pickup.item)

            if wants_to_pickup.collected_by == World.fetch('player'):
                logs = World.fetch('logs')
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_OK}]{Texts.get_text("YOU_PICK_UP")}'
                                f'{Texts.get_text(get_obfuscate_name(wants_to_pickup.item))}[/color]')

        World.remove_component_for_all_entities(WantsToPickUpComponent)
