class ItemComponent:
    pass


class ConsumableComponent:
    def __init__(self, charges=1):
        self.effects = list()
        self.charges = charges


class InBackPackComponent:
    def __init__(self, owner):
        self.owner = owner


class MeleeWeaponComponent:
    def __init__(self, attribute, min_dmg, max_dmg, dmg_bonus, hit_bonus, proc_chance, proc_target):
        self.attribute = attribute
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.dmg_bonus = dmg_bonus
        self.hit_bonus = hit_bonus
        self.proc_chance = proc_chance
        self.proc_target = proc_target


class WearableComponent:
    def __init__(self, armor):
        self.armor = armor
