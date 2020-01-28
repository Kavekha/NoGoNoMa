from world import World
from components.status_effect_components import StatusEffectComponent, DurationComponent, ConfusionComponent, SlowSpellEffect, DamageOverTimeEffect
from components.name_components import NameComponent
from components.equip_components import EquipmentChangedComponent

from effects.targeting_effect import entity_position
from player_systems.game_system import player_gain_xp, calculate_xp_from_entity
from player_systems.on_death import on_player_death
from texts import Texts
import config


def get_slow_effect_name(initiative_penality_value):
    if initiative_penality_value > 0:
        return "SLOW_EFFECT"
    elif initiative_penality_value <= 0:
        return "HASTE_EFFECT"


def add_slow_effect(effect_spawner, target):
    turns = effect_spawner.effect.turns
    slow_effect_name = get_slow_effect_name(effect_spawner.effect.initiative_penality)
    World.create_entity(
        StatusEffectComponent(target),
        SlowSpellEffect(effect_spawner.effect.initiative_penality),
        DurationComponent(nb_turns=turns),
        NameComponent(Texts.get_text(slow_effect_name))
    )
    World.add_component(EquipmentChangedComponent(), target)


def add_damage_over_time_effect(effect_spawner, target):
    turns = effect_spawner.effect.turns
    World.create_entity(
        StatusEffectComponent(target),
        DamageOverTimeEffect(effect_spawner.effect.damage),
        DurationComponent(nb_turns=turns),
        NameComponent(Texts.get_text("DAMAGE_OVER_TIME"))
    )
    World.add_component(EquipmentChangedComponent(), target)


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


def add_confusion_effect(effect_spawner, target):
    turns = effect_spawner.effect.turns
    World.create_entity(StatusEffectComponent(target),
                        ConfusionComponent(),
                        DurationComponent(nb_turns=turns),
                        NameComponent(Texts.get_text("CONFUSION")))
    logs = World.fetch('logs')
    target_named = World.get_entity_component(target, NameComponent).name
    creator_named = World.get_entity_component(effect_spawner.creator, NameComponent).name
    if target_named and creator_named:
        if target_named != creator_named:
            logs.appendleft(f"{creator_named}{Texts.get_text('_INFLICT_CONFUSION_AT_')}{target_named}")
        else:
            logs.appendleft(f"{creator_named}{Texts.get_text('_INFLICT_CONFUSION_ON_THEMSELF')}")
    elif target_named:
        logs.appendleft(f'{target_named}{Texts.get_text("_BECOMES_CONFUSED")}')
