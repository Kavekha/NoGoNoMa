import math

import config


def distance_to(self_position_x, self_position_y, other_position_x, other_position_y):
    dx = other_position_x - self_position_x
    dy = other_position_y - self_position_y
    return math.sqrt(dx ** 2 + dy ** 2)


def index_to_point2d(idx):
    # Transform an idx 1D array to a x, y format for 2D array
    return int(idx % config.MAP_WIDTH), idx // config.MAP_WIDTH


def xy_idx(x, y):
    # Return the map tile (x, y). Avoid List in list [x][y]
    return (y * config.MAP_WIDTH) + x


