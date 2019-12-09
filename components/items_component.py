class ItemComponent:
    pass


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
