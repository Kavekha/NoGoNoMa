from time import perf_counter


class ParticuleLifetimeComponent:
    def __init__(self, lifetime=0.2):
        self.lifetime = lifetime
        self.start_time = perf_counter()


class SpawnParticuleLineComponent:
    def __init__(self, glyph, color, sprite):
        self.glyph = glyph
        self.color = color
        self.sprite = sprite


class SpawnParticuleBurstComponent:
    def __init__(self, glyph, color, sprite):
        self.glyph = glyph
        self.color = color
        self.sprite = sprite
