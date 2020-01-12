class MagicItemComponent:
    def __init__(self, magic_class, naming=None, cursed=False):
        self.magic_class = magic_class
        self.naming = naming
        self.cursed = cursed


class IdentifiedItemComponent:
    def __init__(self, name):
        self.name = name


class CursedItemComponent:
    pass
