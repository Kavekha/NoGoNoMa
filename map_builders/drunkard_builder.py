import tcod

from map_builders.map_builders import MapBuilder
from gmap.gmap_enums import TileType
import config


class DrunkardsWalkBuilder(MapBuilder):
    def __init__(self, depth):
        super().__init__(depth)

    def build(self):
        # starting point
        x, y = self.map.width // 2, self.map.height // 2
        start_idx = self.map.xy_idx(x, y)
        while self.map.tiles[start_idx] != TileType.FLOOR:
            x += 1
            y += 1
            start_idx = self.map.xy_idx(x, y)
        print(f'starting point is {start_idx}, {x, y}')

        # Found an exit
        self.map.create_fov_map()
        dij_path = tcod.path.Dijkstra(self.map.fov_map, 1.41)

        # Compute path from starting position
        best_exit = 0
        best_distance = 0
        for (i, tile) in enumerate(self.map.tiles):
            if tile == TileType.FLOOR:
                exit_tile_x, exit_tile_y = self.map.index_to_point2d(i)
                dij_path.set_goal(exit_tile_x, exit_tile_y)
                my_path = dij_path.get_path(x, y)
                if my_path:
                    if len(my_path) > best_distance:
                        best_exit = i
                        best_distance = len(my_path)

        if best_exit:
            if self.depth != config.MAX_DEPTH:
                self.map.tiles[best_exit] = TileType.DOWN_STAIRS
            else:
                self.map.tiles[best_exit] = TileType.EXIT_PORTAL

            # we can add starting position for player
            self.starting_position = x, y
            self.take_snapshot()

        '''
        for y in range(0, self.map.height - 1):
            for x in range(0, self.map.width - 1):
                idx = self.map.xy_idx(x, y)
                if self.map.tiles[idx] == TileType.FLOOR:
                    cell_value = noise.
        '''

        noise = tcod.noise.Noise(
            dimensions=2,
            algorithm=tcod.NOISE_SIMPLEX,
            implementation=tcod.noise.TURBULENCE,
            hurst=0.5,
            lacunarity=2.0,
            octaves=4,
            seed=None,
        )

        # Create a 5x5 open multi-dimensional mesh-grid.
        ogrid = self.map.fov_map.copy()
        sample = noise.sample_ogrid(ogrid)
        print(ogrid)

        # Scale the grid.
        ogrid[0] *= 0.25
        ogrid[1] *= 0.25

        # Return the sampled noise from this grid of points.
        samples = noise.sample_ogrid(ogrid)
        print(samples)