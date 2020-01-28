class SpellTemplate:
    def __init__(self, mana_cost=0):
        self.mana_cost = mana_cost


class KnownSpell:
    def __init__(self, display_name, mana_cost):
        self.display_name = display_name
        self.mana_cost = mana_cost


class KnownSpells:
    def __init__(self):
        self.spells = list()


class TeachesSpell:
    def __init__(self, spell):
        self.spell = spell
