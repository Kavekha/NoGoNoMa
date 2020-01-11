from enum import Enum
from collections import deque

from systems.system import System


class EffectType(Enum):
    DAMAGE = 0      # {damage:0}


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


class Targets:
    def __init__(self, target_type, **kwargs):
        self.target_type = None

        if target_type == TargetType.SINGLE:
            pass
        elif target_type == TargetType.AREA:
            pass


class EffectSpawner:
    def __init__(self, creator, effect_type, targets):
        self.creator = creator
        self.effect_type = effect_type
        self.targets = targets


class EffectSystem(System):
    EFFECT_QUEUE = deque()

    @classmethod
    def add_effect(cls, creator, effect_type, targets):
        effect_spawner = EffectSpawner(creator, effect_type, targets)
        EffectSystem.EFFECT_QUEUE.appendleft(effect_spawner)

    def update(self, *args, **kwargs):
        while True:
            if EffectSystem.EFFECT_QUEUE:
                effect = EffectSystem.EFFECT_QUEUE.pop()
                print(f'effect queue: effect is {effect}')
            else:
                break
