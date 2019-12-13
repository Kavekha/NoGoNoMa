from time import perf_counter


class ParticuleLifetimeComponent:
    def __init__(self, lifetime=0.2):
        self.lifetime = lifetime
        self.start_time = perf_counter()
