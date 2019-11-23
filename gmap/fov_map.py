import tcod
import config

from gmap.map_creation import Gmap
from data.types import TileType

def index_to_point2d(idx):
    # Transform an idx 1D array to a x, y format for 2D array
    return idx % config.MAP_WIDTH, idx // config.MAP_WIDTH

def xy_idx(x, y):
    # Return the map tile (x, y). Avoid List in list [x][y]
    return (y * config.MAP_WIDTH) + x


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
