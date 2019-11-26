from enum import Enum


class State:
    def __init__(self, state):
        self.current_state = state

    def change_state(self, new_state):
        self.current_state = new_state


class Layers(Enum):
    BACKGROUND = 0
    UNKNOWN = 1
    MAP = 2
    ITEM = 3
    MONSTER = 4
    PLAYER = 5
    INTERFACE = 6
    TOOLTIP = 7
    MENU = 8


class States(Enum):
    AWAITING_INPUT = 0
    PRE_RUN = 1
    PLAYER_TURN = 2
    MONSTER_TURN = 3
    SHOW_INVENTORY = 4
    SHOW_ITEM_WINDOW = 5
    SHOW_DROP_ITEM = 6
    SHOW_TARGETING = 7
    MAIN_MENU = 8
    LOAD_GAME = 9
    SAVE_GAME = 10


class TileType(Enum):
    FLOOR = 0
    WALL = 1


class ItemMenuResult(Enum):
    CANCEL = 0
    NO_RESPONSE = 1
    SELECTED = 2


class MainMenuSelection(Enum):
    NEWGAME = 0
    LOAD_GAME = 1
    QUIT = 2
    NO_RESPONSE = 3
