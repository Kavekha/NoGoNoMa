from map_builders.simple_map_builder import SimpleMapBuilder


def build_random_map(depth):
    map_to_build = SimpleMapBuilder()
    return map_to_build.build(depth)


def spawn(map, depth):
    map_to_spawn = SimpleMapBuilder()
    return  map_to_spawn.spawn(map, depth)
