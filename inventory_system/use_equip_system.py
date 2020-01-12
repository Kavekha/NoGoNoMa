from world import World
from systems.system import System
from components.intent_components import WantsToUseComponent
from components.equip_components import EquippableComponent, EquippedComponent
from components.name_components import NameComponent

from components.item_components import InBackPackComponent
from ui_system.render_functions import get_obfuscate_name
import config
from texts import Texts


class UseEquipSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToUseComponent)
        logs = World.fetch('logs')
        player = World.fetch('player')

        # remove_use = list()   # Pour poser component "equipment changed"
        for entity, (use_item, *args) in subjects:
            can_equip = World.get_entity_component(use_item.item, EquippableComponent)
            if can_equip:
                entity_slot = can_equip.slot

                to_unequip = list()
                item_subjects = World.get_components(EquippedComponent, NameComponent)
                for item_entity, (already_equipped, named_item) in item_subjects:
                    if already_equipped.owner == entity and already_equipped.slot == entity_slot:
                        to_unequip.append(item_entity)
                        if entity == player:
                            logs.appendleft(f'[color={config.COLOR_SYS_MSG}]'
                                            f'{Texts.get_text("YOU_UNEQUIP")}'
                                            f'{Texts.get_text(get_obfuscate_name(item_entity))}[/color]')

                for item in to_unequip:
                    World.remove_component(EquippedComponent, item)
                    World.add_component(InBackPackComponent(owner=entity), item)

                World.add_component(EquippedComponent(owner=use_item.item, equipment_slot=entity_slot), entity)
                World.remove_component(InBackPackComponent, use_item.item)
                if entity == player:
                    logs.appendleft(f'[color={config.COLOR_SYS_MSG}]'
                                    f'{Texts.get_text("YOU_EQUIP")}'
                                    f'{Texts.get_text(get_obfuscate_name(use_item.item))}'
                                    f'[/color]')
                # remove_use.append(entity)

        # World.remove_component_for_all_entities(WantsToUseComponent)


