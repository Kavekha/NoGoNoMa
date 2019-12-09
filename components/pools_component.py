class Pool:
    def __init__(self, max_value):
        self.max = max_value
        self.current = max_value


class Pools:
    def __init__(self, hits, mana, level=1):
        self.hit_points = Pool(hits)
        self.mana_points = Pool(mana)
        self.xp = 0
        self.level = level
