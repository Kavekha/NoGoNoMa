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
