from world import World
from systems.system import System
from components.intent_components import WantsToRemoveItemComponent
from components.magic_item_components import CursedItemComponent
from ui_system.render_functions import get_obfuscate_name
from components.equip_components import EquippedComponent
from components.item_components import InBackPackComponent
from components.name_components import NameComponent
from components.area_effect_component import AreaOfEffectComponent
from effects.effects_system import add_effect, Effect, EffectType, Targets, TargetType
from effects.targeting_effect import get_aoe_tiles
import config
from texts import Texts


class ItemRemoveSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToRemoveItemComponent)

        for entity, (wants_to_remove, *args) in subjects:
            cursed = World.get_entity_component(wants_to_remove.item, CursedItemComponent)
            if cursed:
                logs = World.fetch('logs')
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]'
                                f'{Texts.get_text("YOU_CANNOT_REMOVE_").format(get_obfuscate_name(wants_to_remove.item))}'
                                f'{Texts.get_text("ITS_CURSED")}[/color]')
            else:
                World.remove_component(EquippedComponent, wants_to_remove.item)
                World.add_component(InBackPackComponent(owner=entity), wants_to_remove.item)

        World.remove_component_for_all_entities(WantsToRemoveItemComponent)
