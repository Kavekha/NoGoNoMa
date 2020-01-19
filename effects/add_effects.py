from world import World
from components.status_effect_components import StatusEffectComponent, DurationComponent
from components.name_components import NameComponent
from components.equip_components import EquipmentChangedComponent
from texts import Texts


def add_attribute_effect(effect_spawner, target):
    turns = effect_spawner.effect.turns

    World.create_entity(
        StatusEffectComponent(target),
        effect_spawner.effect.attr_bonus,
        DurationComponent(nb_turns=turns),
        NameComponent(Texts.get_text("ATTRIBUTE_MODIFIER"))
    )
    World.add_component(EquipmentChangedComponent(), target)
