from world import World
from systems.system import System
from components.intent_components import WantsToUseComponent
from components.equip_components import EquippableComponent, EquippedComponent, EquipmentChangedComponent
from components.name_components import NameComponent
from components.magic_item_components import IdentifiedItemComponent, CursedItemComponent
from components.item_components import InBackPackComponent
from ui_system.render_functions import get_obfuscate_name
import config
from texts import Texts


class UseEquipSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToUseComponent)
        logs = World.fetch('logs')
        player = World.fetch('player')

        remove_use = list()
        for entity, (use_item, *args) in subjects:
            can_equip = World.get_entity_component(use_item.item, EquippableComponent)
            if can_equip:
                entity_slot = can_equip.slot

                # if already equiped, we desequip
                to_unequip = list()
                item_subjects = World.get_components(EquippedComponent, NameComponent)
                for item_entity, (already_equipped, named_item) in item_subjects:
                    if already_equipped.owner == entity and already_equipped.slot == entity_slot:
                        cursed = World.get_entity_component(item_entity, CursedItemComponent)
                        if cursed:
                            can_equip = False
                            logs = World.fetch('logs')
                            logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]'
                                            f'{Texts.get_text("YOU_CANNOT_REMOVE_").format(get_obfuscate_name(item_entity))}'
                                            f'{Texts.get_text("ITS_CURSED")}[/color]')
                        else:
                            to_unequip.append(item_entity)
                            if entity == player:
                                logs.appendleft(f'[color={config.COLOR_SYS_MSG}]'
                                                f'{Texts.get_text("YOU_UNEQUIP")}'
                                                f'{Texts.get_text(get_obfuscate_name(item_entity))}[/color]')

                if can_equip:
                    for item in to_unequip:
                        World.remove_component(EquippedComponent, item)
                        World.add_component(InBackPackComponent(owner=entity), item)

                    World.add_component(EquipmentChangedComponent(), entity)
                    World.add_component(EquippedComponent(owner=entity, equipment_slot=entity_slot), use_item.item)
                    World.remove_component(InBackPackComponent, use_item.item)
                    if entity == player:
                        logs.appendleft(f'[color={config.COLOR_SYS_MSG}]'
                                        f'{Texts.get_text("YOU_EQUIP")}'
                                        f'{Texts.get_text(get_obfuscate_name(use_item.item))}'
                                        f'[/color]')

                        # identify
                        item_named = World.get_entity_component(use_item.item, NameComponent)
                        World.add_component(IdentifiedItemComponent(name=item_named.name), entity)

                remove_use.append(entity)

        for entity in remove_use:
            World.remove_component(WantsToUseComponent, entity)
