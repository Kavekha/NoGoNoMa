from bearlibterminal import terminal

from ui_system.item_menu import ItemMenu, ItemMenuType, InventorySelectedMenu
from ui_system.menus import CharacterMenu, MainMenu, GameOverMenu, VictoryMenu, MainOptionsMenu, \
    QuitGameMenu
from texts import Texts


def show_identify_menu():
    identify_menu = ItemMenu(Texts.get_text("IDENTIFY_MENU"), ItemMenuType.IDENTIFY_ITEM)
    identify_menu.initialize()


def show_curse_removal_screen():
    removal_curse_menu = ItemMenu(Texts.get_text("CURSE_REMOVAL_MENU"), ItemMenuType.REMOVAL_CURSE_ON_ITEM)
    removal_curse_menu.initialize()


def show_item_screen():
    inventory_menu = ItemMenu(Texts.get_text("INVENTORY"), ItemMenuType.INVENTORY_MENU)
    inventory_menu.initialize()


def show_selected_item_screen(item):
    inventory_menu = InventorySelectedMenu(Texts.get_text("INVENTORY"),
                                           ItemMenuType.INVENTORY_WITH_SELECT_ITEM_MENU,
                                           item)
    inventory_menu.initialize()


def show_character_menu():
    character_menu = CharacterMenu(Texts.get_text("CHARACTER_SHEET_HEADER"))
    character_menu.initialize()


def show_main_menu():
    terminal.clear()
    main_menu = MainMenu(Texts.get_text("GAME_TITLE"))
    main_menu.initialize()


def show_game_over_menu():
    terminal.clear()
    game_over_menu = GameOverMenu(Texts.get_text("GAME_OVER"))
    game_over_menu.initialize()


def show_victory_menu():
    terminal.clear()
    victory_menu = VictoryMenu(Texts.get_text("VICTORY"))
    victory_menu.initialize()


def show_main_options_menu():
    terminal.clear()
    main_options_menu = MainOptionsMenu(Texts.get_text("OPTIONS_MENU"))
    main_options_menu.initialize()


def show_quit_game_menu():
    quit_game_menu = QuitGameMenu(Texts.get_text("QUIT_GAME_QUESTION"))
    quit_game_menu.initialize()
