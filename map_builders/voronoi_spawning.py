import tcod as tcod

from map_builders.builder_map import MetaMapbuilder
from gmap.gmap_enums import TileType
from gmap.spawner import spawn_region


class VoronoiSpawning(MetaMapbuilder):
    def build_map(self, build_data):
        noise = tcod.noise.Noise(
            dimensions=2,
            algorithm=tcod.NOISE_SIMPLEX,
            implementation=tcod.noise.TURBULENCE,
            hurst=0.5,
            lacunarity=2.0,
            octaves=4,
            seed=None
        )

        noise_areas = dict()
        for y in range(0, build_data.map.height):
            for x in range(0, build_data.map.width):
                if build_data.map.tiles[build_data.map.xy_idx(x, y)] == TileType.FLOOR:
                    # score between 0.99 & 0.5 : 550 at >0.9, 1200 at >8, 0 at > 6 and 200 at < 6.
                    cell_value = noise.get_point(x, y)
                    cell_value_int = int(cell_value * 10)  # so we have enought for 10 areas.
                    if cell_value_int not in noise_areas:
                        noise_areas[cell_value_int] = list()
                    noise_areas[cell_value_int].append(build_data.map.xy_idx(x, y))

        count = 0
        for key, value in noise_areas.items():
            print(f'area {key} - nb of points : {len(value)} idx')
            count += 1
        print(f'number of areas : {count}')

        for area in noise_areas:
            spawn_region(noise_areas[area], build_data.map, build_data.spawn_list)
