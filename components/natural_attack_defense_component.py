class NaturalAttackDefenseComponent:
    def __init__(self, natural_armor=0):
        self.natural_armor = natural_armor
        self.attacks = list()


class NaturalAttack:
    def __init__(self, name, attribute, min_dmg, max_dmg, dmg_bonus, hit_bonus, proc_chance=None, proc_target=None):
        self.name = name
        self.attribute = attribute
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.dmg_bonus = dmg_bonus
        self.hit_bonus = hit_bonus
        self.proc_chance = proc_chance
        self.proc_target = proc_target
