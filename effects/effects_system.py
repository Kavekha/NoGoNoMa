from collections import deque
from enum import Enum
from random import randint

from systems.system import System

from world import World
from effects.targeting_effect import entity_position
from components.pools_component import Pools
import config


class EffectType(Enum):
    DAMAGE = 0      # {damage:0}
    BLOOD_STAINS = 1


class Effect:
    def __init__(self, effect_type, **kwargs):
        self.effect_type = None
        self.damage = None

        if effect_type == EffectType.DAMAGE:
            self.damage = kwargs.get('damage', 0)
        self.effect_type = effect_type


class TargetType(Enum):
    SINGLE = 0
    AREA = 1
    TILE = 2


class Targets:
    def __init__(self, target_type, **kwargs):
        self.target_type = None
        self.target = None

        if target_type == TargetType.SINGLE:
            self.target = kwargs.get('target', 0)
        elif target_type == TargetType.AREA:
            pass
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
    if effect_spawner.targets.target_type == TargetType.SINGLE:
        affect_entity(effect_spawner, effect_spawner.targets.target)


def affect_entity(effect_spawner, target):
    if effect_spawner.effect.effect_type == EffectType.DAMAGE:
        inflict_damage_effect(effect_spawner.effect, target)
    else:
        return


def affect_tile(effect, tile_idx):
    if tile_effect_hits_entity(effect):
        content = World.fetch('current_map').tile_content[tile_idx]
        for entity in content:
            affect_entity(effect, entity)

    if effect.effect_type == EffectType.BLOOD_STAINS:
        inflict_bloodstain(tile_idx)
    else:
        return


def tile_effect_hits_entity(effect):
    if effect.effect_type == EffectType.DAMAGE:
        return True
    else:
        return False


def inflict_damage_effect(effect_spawner_effect, target):
    pool = World.get_entity_component(target, Pools)
    if pool and effect_spawner_effect.effect_type == EffectType.DAMAGE:
        pool.hit_points.current -= effect_spawner_effect.damage

        if randint(0, 100) < config.BLOOD_ON_GROUND_CHANCE:
            tile_idx = entity_position(target)
            add_effect(None, Effect(EffectType.BLOOD_STAINS), Targets(TargetType.TILE, target=tile_idx))


def inflict_bloodstain(tile_idx):
    current_map = World.fetch('current_map')
    current_map.stains[tile_idx] = randint(1, 5)
