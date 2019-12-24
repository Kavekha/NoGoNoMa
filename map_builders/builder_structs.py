from enum import Enum


class DrunkSpawnMode(Enum):
    STARTING_POINT = 0
    RANDOM = 1


class DLAAlgorithm(Enum):
    WALK_INWARDS = 0
    WALK_OUTWARDS = 1
    CENTRAL_ATTRACTOR = 2


class Symmetry(Enum):
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2
    BOTH = 3
