from map_builders.simple_map_builder import SimpleMapBuilder


def random_builder(depth):
    rand = 0
    if rand == 0:
        return SimpleMapBuilder(depth)


def build_random_map(depth):
    map_builder = random_builder(depth)
    map_builder.build_map()
    return map_builder

