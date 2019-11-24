from enum import Enum


class State:
    def __init__(self, state):
        self.current_state = state
        self.data = {}

    def change_state(self, new_state):
        self.current_state = new_state


class Layers(Enum):
    UNKNOWN = 0
    MAP = 1
    ITEM = 2
    MONSTER = 3
    PLAYER = 4
    INTERFACE = 5
    MENU = 6
    AVAILABLE_TILES = 7
    TOOLTIP = 8


class States(Enum):
    AWAITING_INPUT = 0
    PRE_RUN = 1
    PLAYER_TURN = 2
    MONSTER_TURN = 3
    SHOW_INVENTORY = 4
    SHOW_ITEM_WINDOW = 5
    SHOW_DROP_ITEM = 6
    SHOW_TARGETING = 7


class TileType(Enum):
    FLOOR = 0
    WALL = 1


class ItemMenuResult(Enum):
    CANCEL = 0
    NO_RESPONSE = 1
    SELECTED = 2
