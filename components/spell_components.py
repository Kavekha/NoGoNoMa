class SpellTemplate:
    def __init__(self, mana_cost):
        self.mana_cost = mana_cost


class KnownSpell:
    def __init__(self, display_name, mana_cost):
        self.display_name = display_name
        self.mana_cost = mana_cost


class KnownSpells:
    def __init__(self):
        self.spells = list()
