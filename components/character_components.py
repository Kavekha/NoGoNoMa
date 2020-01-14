class Stat:
    def __init__(self, original_value):
        self.value = original_value
        self.bonus_value = original_value


class AttributesComponent:
    def __init__(self, might, body, quickness, wits):
        self.might = Stat(might)
        self.body = Stat(body)
        self.quickness = Stat(quickness)
        self.wits = Stat(wits)


class MonsterComponent:
    pass


class PlayerComponent:
    def __init__(self):
        pass


class AutopickupComponent:
    pass
