from enum import Enum


class ItemMenuResult(Enum):
    CANCEL = 0
    NO_RESPONSE = 1
    SELECTED = 2


class NextLevelResult(Enum):
    NO_EXIT = 0
    NEXT_FLOOR = 1
    EXIT_DUNGEON = 2


class MainMenuSelection(Enum):
    NEWGAME = 0
    LOAD_GAME = 1
    QUIT = 2
    NO_RESPONSE = 3


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