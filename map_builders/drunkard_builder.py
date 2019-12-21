import tcod

from map_builders.map_builders import MapBuilder
from gmap.gmap_enums import TileType


class DrunkardsWalkBuilder(MapBuilder):
    def __init__(self, depth):
        super().__init__(depth)

    def build(self):
        starting_position = self.map.width // 2, self.map.height // 2
        start_idx = self.map.xy_idx(starting_position[0], starting_position[1])

        self.map.tiles = [TileType.FLOOR] * (self.map.height * self.map.width)

        tcod_map = tcod.map.Map(self.map.width, self.map.height)
        for i, tile in enumerate(self.map.tiles):
            x, y = self.map.index_to_point2d(i)
            if tile != TileType.WALL:
                tcod_map.walkable[y, x] = True
            else:
                tcod_map.walkable[y, x] = False

        dij_path = tcod.path.Dijkstra(tcod_map, 1.41)
        dij_path.set_goal(10, 10)
        move_list = dij_path.get_path(20, 20)
        print(f'get path list is {move_list}')


if __name__ == '__main__':
    builder = DrunkardsWalkBuilder(1)
    builder.build()
