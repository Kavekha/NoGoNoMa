import tcod
import config

from gmap.map_creation import Gmap
from gmap.utils import index_to_point2d
from data.types import TileType

gmap = Gmap()
gmap.fov_map = tcod.map.Map(config.MAP_WIDTH, config.MAP_HEIGHT)


print(f'gmap is {gmap.tiles}')
for _i in range(len(gmap.tiles) -1):
    if gmap.tiles[_i] != TileType.WALL:
        x, y = index_to_point2d(_i)
        gmap.fov_map.transparent[y, x] = True


print(f'map walkable is : {gmap.fov_map.walkable}')

gmap.fov_map.compute_fov(0, 0, 6, False)
print(f'fov is {gmap.fov_map.fov}')
