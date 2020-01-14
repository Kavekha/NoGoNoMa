class ItemComponent:
    pass


class ConsumableComponent:
    pass


class InBackPackComponent:
    def __init__(self, owner):
        self.owner = owner


class MeleeWeaponComponent:
    def __init__(self, attribute, min_dmg, max_dmg, dmg_bonus, hit_bonus):
        self.attribute = attribute
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.dmg_bonus = dmg_bonus
        self.hit_bonus = hit_bonus


class WearableComponent:
    def __init__(self, armor):
        self.armor = armor


class ItemAttributeBonusComponent:
    def __init__(self, might=0, body=0, quickness=0, wits=0):
        self.might = might
        self.body = body
        self.quickness = quickness
        self.wits = wits
