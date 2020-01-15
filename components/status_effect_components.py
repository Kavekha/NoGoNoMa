class ConfusionComponent:
    pass


class DurationComponent:
    def __init__(self, nb_turns):
        self.turns = nb_turns


class StatusEffectComponent:
    def __init__(self, target):
        self.target = target
