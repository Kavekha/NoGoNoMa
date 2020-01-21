from world import World
from components.status_effect_components import StatusEffectComponent, DurationComponent
from components.name_components import NameComponent
from components.equip_components import EquipmentChangedComponent

from effects.targeting_effect import entity_position
from player_systems.game_system import player_gain_xp, calculate_xp_from_entity
from player_systems.on_death import on_player_death
from texts import Texts
import config


def add_attribute_effect(effect_spawner, target):
    turns = effect_spawner.effect.turns
    World.create_entity(
        StatusEffectComponent(target),
        effect_spawner.effect.attr_bonus,
        DurationComponent(nb_turns=turns),
        NameComponent(Texts.get_text("ATTRIBUTE_MODIFIER"))
    )
    World.add_component(EquipmentChangedComponent(), target)


def death_effect(effect_spawner, target):
    # remove
    current_map = World.fetch('current_map')
    target_pos = entity_position(target)
    current_map.blocked_tiles[target_pos] = False

    name = World.get_entity_component(target, NameComponent)
    logs = World.fetch('logs')
    logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]'
                    f'{Texts.get_text("_HAS_BEEN_SLAIN").format(Texts.get_text(name.name))}[/color]')

    if effect_spawner.creator == World.fetch('player'):
        player_gain_xp(calculate_xp_from_entity(target))

    if target == World.fetch('player'):
        on_player_death()
    else:
        World.delete_entity(target)