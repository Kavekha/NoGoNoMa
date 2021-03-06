from collections import deque
from enum import Enum
from random import randint

from systems.system import System
from systems.particule_system import ParticuleBuilder
from world import World

from effects.targeting_effect import entity_position, find_item_position
from effects.add_effects import add_attribute_effect, death_effect, add_confusion_effect, add_damage_over_time_effect,\
    add_slow_effect

from components.pools_component import Pools
from components.provide_effects_components import ProvidesHealingComponent, ProvidesCurseRemovalComponent, \
    ProvidesIdentificationComponent, ProvidesManaComponent
from components.item_components import ConsumableComponent
from components.status_effect_components import ConfusionComponent, DurationComponent, StatusEffectComponent, \
    SlowSpellEffect, DamageOverTimeEffect
from components.hidden_component import HiddenComponent
from components.triggers_components import ActivationComponent
from components.inflicts_damage_component import InflictsDamageComponent
from components.initiative_components import InitiativeCostComponent
from components.particule_components import SpawnParticuleBurstComponent, SpawnParticuleLineComponent
from components.character_components import AttributeBonusComponent
from components.spell_components import TeachesSpell, KnownSpells, KnownSpell, SpellTemplate
from data_raw_master.load_raws import find_spell_entity

from state import States
from inventory_system.inventory_functions import get_non_identify_items_in_inventory, \
    get_known_cursed_items_in_inventory
from player_systems.game_system import get_obfuscate_name
from components.name_components import NameComponent
from texts import Texts

import config

"""
DOCUMENTATION:
    -- Usage:
        add_effect(source, Effect(EffectType, args du type), Targets(TargetType, args))

    -- Creer un effet.
        * Ajouter EffectType
            exemple: HEALING
        * Dans Effect: a l'init, ajouter les args necessaires pour ce EffectType.
            exemple: if HEALING, self.amount = kwargs.get('amount')
        * Ajouter TargetType
            exemple: TILE
        * dans Targets: A l'init, ajouter la target pour ce TargetType.
            exemple: if TILE, self.target = kwargs.get('tile')
        * Ajouter le TargetType dans target_applicator.
            Quand l'effet est recuperé par la Queue, la fonction target_applicator est utilisée.
            Une fonction est jouée selon le target_applicator.
        * Ajouter pour ce TargetType, dans target_applicator, la fonction à utiliser.
            Exemple: affect_tile
        * Dans la fonction affect_tile, check si l'EffectType est utilisable sur les entitées de cette Tile.
        * Dans la fonction affect_tile, check l'EffectType et utilise la vraie Fonction liée à l'effet.
        * Creer enfin le vrai effet, avec les infos recupérés ici et là.

"""


class EffectType(Enum):
    DAMAGE = 0  # {damage:0}
    BLOOD_STAINS = 1
    PARTICULE = 2
    ENTITY_DEATH = 3
    ITEM_USE = 4
    HEALING = 5
    CONFUSION = 6
    TRIGGER_FIRE = 7
    ATTRIBUTE_EFFECT = 8
    SPELL_USE = 9
    MANA = 10
    SLOW = 11
    DAMAGE_OVER_TIME = 12


class Effect:
    def __init__(self, effect_type, **kwargs):
        self.effect_type = None
        self.damage = None

        if effect_type == EffectType.DAMAGE:
            self.damage = kwargs.get('damage', 0)

        elif effect_type == EffectType.PARTICULE:
            self.glyph = kwargs.get('glyph')
            self.fg = kwargs.get('fg')
            self.sprite = kwargs.get('sprite')
            self.lifetime = kwargs.get('lifetime')

        elif effect_type == EffectType.ITEM_USE:
            self.item = kwargs.get('item')

        elif effect_type == EffectType.HEALING:
            self.amount = kwargs.get('amount')

        elif effect_type == EffectType.CONFUSION:
            self.turns = kwargs.get('turns')

        elif effect_type == EffectType.TRIGGER_FIRE:
            self.trigger = kwargs.get('trigger')

        elif effect_type == EffectType.ATTRIBUTE_EFFECT:
            self.attr_bonus = kwargs.get('attribute_bonus_component')
            self.turns = kwargs.get('turns')

        elif effect_type == EffectType.SPELL_USE:
            self.spell = kwargs.get('spell')

        elif effect_type == EffectType.MANA:
            self.mana_amount = kwargs.get('amount')

        elif effect_type == EffectType.SLOW:
            self.initiative_penality = kwargs.get('initiative_penality')
            self.turns = kwargs.get('turns')

        elif effect_type == EffectType.DAMAGE_OVER_TIME:
            self.damage = kwargs.get('damage')
            self.turns = kwargs.get('turns')

        self.effect_type = effect_type


class TargetType(Enum):
    SINGLE = 0
    TILE = 1
    TILES = 2


class Targets:
    def __init__(self, target_type, **kwargs):
        self.target_type = None
        self.target = None

        if target_type == TargetType.SINGLE:
            self.target = kwargs.get('target', 0)
        elif target_type == TargetType.TILE:
            self.target = kwargs.get('tile', None)
        elif target_type == TargetType.TILES:
            self.target = kwargs.get('tiles', None)
        self.target_type = target_type


class EffectSpawner:
    def __init__(self, creator, effect, targets):
        self.creator = creator
        self.effect = effect
        self.targets = targets


class EffectSystem(System):
    EFFECT_QUEUE = deque()

    def update(self, *args, **kwargs):
        while True:
            if EffectSystem.EFFECT_QUEUE:
                effect_spawner = EffectSystem.EFFECT_QUEUE.pop()
                target_applicator(effect_spawner)
            else:
                break


def add_effect(creator, effect_type, targets):
    effect_spawner = EffectSpawner(creator, effect_type, targets)
    print(f'effect added : from {creator} with type {effect_type.effect_type} and target {targets.target_type}')
    EffectSystem.EFFECT_QUEUE.appendleft(effect_spawner)


def target_applicator(effect_spawner):
    print(f'target applicator: {effect_spawner.targets.target_type}, with target : {effect_spawner.targets.target}')
    print(f'target application: effect is {effect_spawner.effect.effect_type}')
    if effect_spawner.effect.effect_type == EffectType.ITEM_USE:
        item_trigger(effect_spawner.creator, effect_spawner.effect.item, effect_spawner.targets)
    elif effect_spawner.effect.effect_type == EffectType.SPELL_USE:
        spell_trigger(effect_spawner.creator, effect_spawner.effect.spell, effect_spawner.targets)
    elif effect_spawner.effect.effect_type == EffectType.TRIGGER_FIRE:
        trigget_fire(effect_spawner.creator, effect_spawner.effect.trigger, effect_spawner.targets)
    else:
        # cible unique
        if effect_spawner.targets.target_type == TargetType.SINGLE:
            affect_entity(effect_spawner, effect_spawner.targets.target)
        # tuile
        elif effect_spawner.targets.target_type == TargetType.TILE:
            affect_tile(effect_spawner, effect_spawner.targets.target)
        # aoe
        elif effect_spawner.targets.target_type == TargetType.TILES:
            print(f'target applicator: aoe: target is : {effect_spawner.targets.target}')
            affect_multiple_tiles(effect_spawner, effect_spawner.targets.target)
            # affect_tile(effect_spawner, effect_spawner.targets.target)


def trigget_fire(creator, trigger, effect_spawner_target):
    # no longer hidden
    hidden = World.get_entity_component(trigger, HiddenComponent)
    if hidden:
        World.remove_component(HiddenComponent, trigger)

    # launch event
    did_something = event_trigger(creator, trigger, effect_spawner_target)

    # remove activation
    trigger_activation = World.get_entity_component(trigger, ActivationComponent)
    if trigger_activation and did_something:
        trigger_activation.nb_activations -= 1
        if trigger_activation.nb_activations < 1:
            World.delete_entity(trigger)


def spell_trigger(creator, spell, effect_spawner_target):
    from components.spell_components import SpellTemplate
    spell_casted = World.get_entity_component(spell, SpellTemplate)
    print(f'spell caster is : {spell_casted}.')
    print(f'Mana cost is {spell_casted.mana_cost}')
    if spell_casted and creator:
        caster_pools = World.get_entity_component(creator, Pools)
        if caster_pools:
            if spell_casted.mana_cost <= caster_pools.mana_points.current:
                caster_pools.mana_points.current -= spell_casted.mana_cost
    event_trigger(creator, spell, effect_spawner_target)


def item_trigger(creator, item, effect_spawner_target):
    # item has charge?
    item_consumable = World.get_entity_component(item, ConsumableComponent)
    if item_consumable:
        if item_consumable.charges < 1:
            logs = World.fetch('logs')
            item_name = get_obfuscate_name(item)
            logs.appendleft(f'{item_name} {Texts.get_text("_IS_OUT_OF_CHARGES")}')
            return
        else:
            item_consumable.charges -= 1

    # use item via generic system
    did_something = event_trigger(creator, item, effect_spawner_target)

    if did_something:
        World.add_component(InitiativeCostComponent(config.DEFAULT_ITEM_USE_INITIATIVE_COST), creator)
        if item_consumable:
            if item_consumable.charges == 0:
                World.delete_entity(item)


def event_trigger(creator, item, effect_spawner_target):
    did_something = False

    # particule spawn
    particule_blast = World.get_entity_component(item, SpawnParticuleBurstComponent)
    if particule_blast:
        add_effect(creator, Effect(EffectType.PARTICULE, glyph=particule_blast.glyph,
                                   fg=particule_blast.color,
                                   sprite=particule_blast.sprite),
                   effect_spawner_target)

    # line particule spawn
    particule_line = World.get_entity_component(item, SpawnParticuleLineComponent)
    if particule_line:

        start_pos = find_item_position(item, creator)
        if effect_spawner_target.target_type == TargetType.TILE:
            spawn_line_particules(start_pos, effect_spawner_target.target, particule_line)
        elif effect_spawner_target.target_type == TargetType.TILES:
            for tile in effect_spawner_target.target:
                spawn_line_particules(start_pos, tile, particule_line)
        elif effect_spawner_target.target_type == TargetType.SINGLE:
            end_pos = entity_position(effect_spawner_target.target)
            if end_pos:
                spawn_line_particules(start_pos, end_pos, particule_line)

    # effects
    healing = World.get_entity_component(item, ProvidesHealingComponent)
    damaging = World.get_entity_component(item, InflictsDamageComponent)
    confusion = World.get_entity_component(item, ConfusionComponent)
    remove_curse = World.get_entity_component(item, ProvidesCurseRemovalComponent)
    identify = World.get_entity_component(item, ProvidesIdentificationComponent)
    attr_modifier = World.get_entity_component(item, AttributeBonusComponent)
    mana = World.get_entity_component(item, ProvidesManaComponent)
    teach_spell = World.get_entity_component(item, TeachesSpell)
    dot = World.get_entity_component(item, DamageOverTimeEffect)
    slow = World.get_entity_component(item, SlowSpellEffect)

    if dot:
        dot_duration = World.get_entity_component(item, DurationComponent)
        add_effect(creator,
                   Effect(EffectType.DAMAGE_OVER_TIME, damage=dot.damage, turns=dot_duration.turns),
                   effect_spawner_target)
        did_something = True

    if slow:
        slow_duration = World.get_entity_component(item, DurationComponent)
        add_effect(creator,
                   Effect(EffectType.SLOW, initiative_penality=slow.initiative_penality, turns=slow_duration.turns),
                   effect_spawner_target)
        did_something = True

    if healing:
        add_effect(creator,
                   Effect(EffectType.HEALING, amount=healing.healing_amount),
                   effect_spawner_target)
        did_something = True

    if teach_spell:
        if creator:
            known_spells_comp = World.get_entity_component(creator, KnownSpells)
            spell_to_learn_name = teach_spell.spell
            print(f'spell to learn name is {spell_to_learn_name}')
            spell_template = find_spell_entity(teach_spell.spell)
            spell_template = World.get_entity_component(spell_template, SpellTemplate)
            print(f'spell template is {spell_template}')
            already_known = False
            for spell in known_spells_comp.spells:
                if spell.display_name == spell_to_learn_name:
                    already_known = True
            logs = World.fetch('logs')
            if not already_known:
                known_spells_comp.spells.append(KnownSpell(spell_to_learn_name, spell_template.mana_cost))
                logs.appendleft(f'[color={config.COLOR_SYS_MSG}]{Texts.get_text("YOU_LEARN_SPELL_")}'
                                f'{Texts.get_text(spell_to_learn_name)}[/color]')
                did_something = True
            else:
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]'
                                f'{Texts.get_text("YOU_ALREADY_KNOW_SPELL")}[/color]')

    if mana:
        add_effect(creator,
                   Effect(EffectType.MANA, amount=mana.mana_amount),
                   effect_spawner_target)
        did_something = True

    if damaging:
        add_effect(creator,
                   Effect(EffectType.DAMAGE, damage=damaging.damage),
                   effect_spawner_target)
        did_something = True

    if confusion:
        confusion_duration = World.get_entity_component(item, DurationComponent)
        add_effect(creator,
                   Effect(EffectType.CONFUSION, turns=confusion_duration.turns),
                   effect_spawner_target)
        did_something = True

    if remove_curse:
        # show_curse_removal_screen()   # The show curse disappears when state change, since we dont come from tick.
        run_state = World.fetch('state')
        print(f'we are launching remove curse effect: state is {run_state.current_state}')
        run_state.change_state(States.SHOW_REMOVE_CURSE)
        # we cant know if usage worked or not -_-
        if get_known_cursed_items_in_inventory(creator):
            did_something = True

    if identify:
        # show_identify_screen()   # The show curse disappears when state change, since we dont come from tick.
        run_state = World.fetch('state')
        run_state.change_state(States.SHOW_IDENTIFY_MENU)
        # we cant know if usage worked or not -_-
        # si il y a au moins des items a identifier
        if get_non_identify_items_in_inventory(creator):
            did_something = True

    if attr_modifier:
        attr_duration = config.DEFAULT_ITEM_ATTRIBUTE_MODIFIER_DURATION
        attribute_bonus_component = World.get_entity_component(item, AttributeBonusComponent)
        add_effect(creator,
                   Effect(EffectType.ATTRIBUTE_EFFECT,
                          turns=attr_duration,
                          attribute_bonus_component=attribute_bonus_component),
                   effect_spawner_target)
        did_something = True

    return did_something


def spawn_line_particules(start_idx, end_idx, particule_component):
    from tcod import tcod
    current_map = World.fetch('current_map')
    start_x, start_y = current_map.index_to_point2d(start_idx)
    end_x, end_y = current_map.index_to_point2d(end_idx)

    line = tcod.line_iter(start_x, start_y, end_x, end_y)
    for cell in line:
        x, y = cell
        cell_idx = current_map.xy_idx(x, y)
        print(f'spawn line particules: cell idx is {cell_idx}')
        add_effect(None,
                   Effect(EffectType.PARTICULE, glyph=particule_component.glyph,
                          fg=particule_component.color,
                          sprite=particule_component.sprite),
                   Targets(TargetType.TILE, tile=cell_idx))


def affect_entity(effect_spawner, target):
    if effect_spawner.effect.effect_type == EffectType.DAMAGE:
        inflict_damage_effect(effect_spawner, target)
    elif effect_spawner.effect.effect_type == EffectType.BLOOD_STAINS:
        idx = entity_position(target)
        inflict_bloodstain(idx)
    elif effect_spawner.effect.effect_type == EffectType.PARTICULE:
        idx = entity_position(target)
        particule_to_tile(effect_spawner, idx)
    elif effect_spawner.effect.effect_type == EffectType.ENTITY_DEATH:
        death_effect(effect_spawner, target)
    elif effect_spawner.effect.effect_type == EffectType.HEALING:
        heal_damage_effect(effect_spawner, target)
    elif effect_spawner.effect.effect_type == EffectType.MANA:
        restore_mana(effect_spawner, target)
    elif effect_spawner.effect.effect_type == EffectType.CONFUSION:
        add_confusion_effect(effect_spawner, target)
    elif effect_spawner.effect.effect_type == EffectType.ATTRIBUTE_EFFECT:
        add_attribute_effect(effect_spawner, target)
    elif effect_spawner.effect.effect_type == EffectType.SLOW:
        add_slow_effect(effect_spawner, target)
    elif effect_spawner.effect.effect_type == EffectType.DAMAGE_OVER_TIME:
        add_damage_over_time_effect(effect_spawner, target)
    else:
        return


def affect_multiple_tiles(effect_spawner, tiles):
    for tile in tiles:
        affect_tile(effect_spawner, tile)


def affect_tile(effect_spawner, tile_idx):
    if tile_effect_hits_entity(effect_spawner):
        content = World.fetch('current_map').tile_content[tile_idx]
        for entity in content:
            affect_entity(effect_spawner, entity)

    if effect_spawner.effect.effect_type == EffectType.BLOOD_STAINS:
        inflict_bloodstain(tile_idx)
    elif effect_spawner.effect.effect_type == EffectType.PARTICULE:
        particule_to_tile(effect_spawner, tile_idx)
    else:
        return


def tile_effect_hits_entity(effect_spawner):
    if effect_spawner.effect.effect_type == EffectType.DAMAGE:
        return True
    elif effect_spawner.effect.effect_type == EffectType.HEALING:
        return True
    elif effect_spawner.effect.effect_type == EffectType.CONFUSION:
        return True
    elif effect_spawner.effect.effect_type == EffectType.ATTRIBUTE_EFFECT:
        return True
    elif effect_spawner.effect.effect_type == EffectType.MANA:
        return True
    elif effect_spawner.effect.effect_type == EffectType.SLOW:
        return True
    elif effect_spawner.effect.effect_type == EffectType.DAMAGE_OVER_TIME:
        return True
    else:
        return False


def inflict_damage_effect(effect_spawner, target):
    effect_spawner_effect = effect_spawner.effect
    pool = World.get_entity_component(target, Pools)
    # pool & dmg effect
    if pool and effect_spawner_effect.effect_type == EffectType.DAMAGE:
        pool.hit_points.current -= effect_spawner_effect.damage
        logs = World.fetch('logs')
        creator = effect_spawner.creator
        target_name = World.get_entity_component(target, NameComponent)
        if creator:
            creator_name = World.get_entity_component(creator, NameComponent)
            if creator_name and target_name:
                logs.appendleft(
                    f'{Texts.get_text("HITS_FOR_DMG").format(Texts.get_text(creator_name.name), Texts.get_text(target_name.name), effect_spawner_effect.damage)}')
        elif target_name:
            logs.appendleft(
                f'{Texts.get_text("UNKNOWN_SOURCE_HITS_SOMEONE_FOR_").format(Texts.get_text(target_name.name), effect_spawner_effect.damage)}')

        # blood stain
        if randint(0, 100) < config.BLOOD_ON_GROUND_CHANCE:
            add_effect(None, Effect(EffectType.BLOOD_STAINS), Targets(TargetType.SINGLE, target=target))

        # particule dmg
        add_effect(None, Effect(EffectType.PARTICULE,
                                glyph='!!',
                                fg=config.COLOR_PARTICULE_HIT,
                                sprite='particules/attack.png',
                                lifetime=1),
                   Targets(TargetType.SINGLE, target=target))

        if pool.hit_points.current < 1:
            add_effect(effect_spawner.creator,
                       Effect(EffectType.ENTITY_DEATH),
                       Targets(TargetType.SINGLE, target=target))


def inflict_bloodstain(tile_idx):
    current_map = World.fetch('current_map')
    current_map.stains[tile_idx] = randint(1, 5)


def particule_to_tile(effect_spawner, tile_idx):
    print(f'particule to tile is : {effect_spawner}')
    print(f'particule to tile: tile idx is {tile_idx}')
    if effect_spawner.effect.effect_type == EffectType.PARTICULE:
        current_map = World.fetch('current_map')
        x, y = current_map.index_to_point2d(tile_idx)
        ParticuleBuilder.request(x, y,
                                 effect_spawner.effect.fg,
                                 effect_spawner.effect.glyph, effect_spawner.effect.sprite)





def heal_damage_effect(effect_spawner, target):
    pool = World.get_entity_component(target, Pools)
    if pool:
        if effect_spawner.effect.effect_type == EffectType.HEALING:
            heal_effect = min(pool.hit_points.max,
                              pool.hit_points.current + effect_spawner.effect.amount) - pool.hit_points.current
            pool.hit_points.current += heal_effect
            add_effect(None,
                       Effect(EffectType.PARTICULE,
                              glyph='!',
                              fg=config.COLOR_PARTICULE_HEAL,
                              sprite='particules/heal.png'),
                       Targets(TargetType.SINGLE, target=target))
            logs = World.fetch('logs')
            logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_OK}]'
                            f'{Texts.get_text("YOU_ARE_HEAL_FOR").format(heal_effect)}[/color]')


def restore_mana(effect_spawner, target):
    from components.pools_component import Pools
    pool = World.get_entity_component(target, Pools)
    if pool:
        mana_restore = min(pool.mana_points.max,
                           pool.mana_points.current + effect_spawner.effect.mana_amount) - pool.mana_points.current
        pool.mana_points.current += mana_restore
        add_effect(None,
                   Effect(EffectType.PARTICULE,
                          glyph='!',
                          fg=config.COLOR_PARTICULE_HEAL,
                          sprite='particules/heal.png'),
                   Targets(TargetType.SINGLE, target=target))
        logs = World.fetch('logs')
        logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_OK}]'
                        f'{Texts.get_text("YOUR_MANA_IS_RESTORED_FOR_POINTS").format(mana_restore)}[/color]')