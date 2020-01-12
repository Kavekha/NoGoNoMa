from collections import deque
from enum import Enum
from random import randint
from itertools import product as it_product

from systems.system import System
from systems.particule_system import ParticuleBuilder
from world import World
from effects.targeting_effect import entity_position
from components.pools_component import Pools
from components.provides_healing_component import ProvidesHealingComponent
from components.item_components import ConsumableComponent

from player_systems.game_system import calculate_xp_from_entity, player_gain_xp
from player_systems.on_death import on_player_death
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
    DAMAGE = 0      # {damage:0}
    BLOOD_STAINS = 1
    PARTICULE = 2
    ENTITY_DEATH = 3
    ITEM_USE = 4
    HEALING = 5


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
    if effect_spawner.effect.effect_type == EffectType.ITEM_USE:
        item_trigger(effect_spawner.creator, effect_spawner.effect.item, effect_spawner.targets)
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
            #affect_tile(effect_spawner, effect_spawner.targets.target)


def item_trigger(creator, item, effect_spawner_target):
    # use item via generic system
    event_trigger(creator, item, effect_spawner_target)
    if World.get_entity_component(item, ConsumableComponent):
        World.delete_entity(item)


def event_trigger(creator, item, effect_spawner_target):
    from components.inflicts_damage_component import InflictsDamageComponent

    # healing
    healing = World.get_entity_component(item, ProvidesHealingComponent)
    damaging = World.get_entity_component(item, InflictsDamageComponent)
    if healing:
        add_effect(creator,
                   Effect(EffectType.HEALING, amount=healing.healing_amount),
                   effect_spawner_target)
    if damaging:
        add_effect(creator,
                   Effect(EffectType.DAMAGE, damage=damaging.damage),
                   effect_spawner_target)


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
        particule_to_tile(tile_idx, effect_spawner)
    else:
        return


def tile_effect_hits_entity(effect_spawner):
    if effect_spawner.effect.effect_type == EffectType.DAMAGE:
        return True
    elif effect_spawner.effect.effect_type == EffectType.HEALING:
        return True
    else:
        return False


def inflict_damage_effect(effect_spawner, target):
    effect_spawner_effect = effect_spawner.effect
    pool = World.get_entity_component(target, Pools)
    # pool & dmg effect
    if pool and effect_spawner_effect.effect_type == EffectType.DAMAGE:
        pool.hit_points.current -= effect_spawner_effect.damage

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
    if effect_spawner.effect.effect_type == EffectType.PARTICULE:
        current_map = World.fetch('current_map')
        x, y = current_map.index_to_point2d(tile_idx)
        ParticuleBuilder.request(x, y,
                                 effect_spawner.effect.fg,
                                 effect_spawner.effect.glyph, effect_spawner.effect.sprite)


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


def get_aoe_tiles(target, aoe_radius):
    blast_tiles_idx = list()
    current_map = World.fetch('current_map')

    target_x, target_y = target
    idx = current_map.xy_idx(target_x, target_y)
    radius = aoe_radius // 2

    for x, y in it_product(range(- radius, radius + 1), range(- radius, radius + 1)):
        radius_x = target_x + x
        radius_y = target_y + y
        new_idx = current_map.xy_idx(radius_x, radius_y)
        if not current_map.out_of_bound(new_idx):
            blast_tiles_idx.append(new_idx)

    return blast_tiles_idx


def heal_damage_effect(effect_spawner, target):
    pool = World.get_entity_component(target, Pools)
    if pool:
        if effect_spawner.effect.effect_type == EffectType.HEALING:
            pool.hit_points.current = min(pool.hit_points.max, pool.hit_points.current + effect_spawner.effect.amount)
            add_effect(None,
                       Effect(EffectType.PARTICULE,
                              glyph='!',
                              fg=config.COLOR_PARTICULE_HEAL,
                              sprite='particules/heal.png'),
                       Targets(TargetType.SINGLE, target=target))
