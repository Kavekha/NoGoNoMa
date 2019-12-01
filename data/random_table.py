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
        return None


def room_table(current_depth=0):
    table = RandomTable()
    table.add("morblin", 10 + current_depth)
    table.add("orcish", 2 + current_depth)
    table.add("health potion", 7 + current_depth)
    table.add('missile Magic Scroll', 4 + current_depth)
    table.add("fireball scroll", 2 + current_depth)
    table.add('confusion scroll', 2 + current_depth)
    table.add('dagger', 3)
    table.add('shield', 2)
    table.add('longsword', current_depth - 1)
    table.add('tower shield', current_depth - 1)

    return table
