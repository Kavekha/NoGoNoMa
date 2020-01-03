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
    OPTION = 3
    NO_RESPONSE = 4


class OptionMenuSelection(Enum):
    CHANGE_LANGUAGE = 0
    CHANGE_GRAPHICAL_MODE = 1
    BACK_TO_MAIN_MENU = 2
    NO_RESPONSE = 3


class Layers(Enum):
    BACKGROUND = 0
    UNKNOWN = 1
    MAP = 2
    STAINS = 3
    ITEM = 4
    MONSTER = 5
    PLAYER = 6
    PARTICULE = 7
    INTERFACE = 8
    TOOLTIP = 9
    BACKGROUND_MENU = 10
    MENU = 11
