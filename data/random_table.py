from random import randint


class RandomEntry:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight


class RandomTable:
    def __init__(self, current_depth=1):
        self.entries = []
        self.total_weight = 0
        self.current_depth = current_depth

    def add(self, name, weight):
        if weight > 0:
            self.entries.append(RandomEntry(name, weight))
            self.total_weight += weight

    def roll(self):
        if not self.total_weight:
            return None
        roll = randint(1, self.total_weight) - 1
        index = 0

        while roll > 0:
            if roll < self.entries[index].weight:
                return self.entries[index].name

            roll -= self.entries[index].weight
            index += 1


def room_table(current_depth=0):
    table = RandomTable()
    table.add("MORBLIN", 10 + current_depth)
    table.add("OOGLOTH", 2 + current_depth)
    table.add("HEALTH_POTION", 7 + current_depth)
    table.add('MISSILE_MAGIC_SCROLL', 4 + current_depth)
    table.add("FIREBALL_SCROLL", 2 + current_depth)
    table.add('CONFUSION_SCROLL', 2 + current_depth)
    table.add('DAGGER', 3)
    table.add('BUCKLET', 2)
    table.add('LONGSWORD', current_depth - 1)
    table.add('TOWER_SHIELD', current_depth - 1)

    return table
