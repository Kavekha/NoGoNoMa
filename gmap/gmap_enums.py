from enum import Enum


class TileType(Enum):
    FLOOR = 0
    WALL = 1
    DOWN_STAIRS = 2
    EXIT_PORTAL = 3


class StartX(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class StartY(Enum):
    TOP = 0
    CENTER = 1
    BOTTOM = 2
