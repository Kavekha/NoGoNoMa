class ConfusionComponent:
    pass


class DurationComponent:
    def __init__(self, nb_turns):
        self.turns = nb_turns


class StatusEffectComponent:
    def __init__(self, target):
        self.target = target


class SlowSpellEffect:
    def __init__(self, initiative_penality):
        self.initiative_penality = initiative_penality


class DamageOverTimeEffect:
    def __init__(self, damage):
        self.damage = damage
