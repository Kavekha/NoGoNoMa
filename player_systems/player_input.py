from bearlibterminal import terminal
from player_systems.try_move_player import try_move_player, try_next_level
from systems.inventory_system import get_item
from state import States
from ui_system.ui_enums import NextLevelResult, ItemMenuResult, MainMenuSelection
from new_ui.interface import Interface
from world import World
from texts import Texts
from components.targeting_component import TargetingComponent
import config


def player_input():
    if terminal.has_input():
        key = terminal.read()

        if key == terminal.TK_LEFT or key == terminal.TK_KP_4 or key == terminal.TK_H:
            try_move_player(-1, 0)
        elif key == terminal.TK_RIGHT or key == terminal.TK_KP_6 or key == terminal.TK_L:
            try_move_player(1, 0)
        elif key == terminal.TK_UP or key == terminal.TK_KP_8 or key == terminal.TK_K:
            try_move_player(0, -1)
        elif key == terminal.TK_DOWN or key == terminal.TK_KP_2 or key == terminal.TK_J:
            try_move_player(0, 1)
        #diagonal
        elif key == terminal.TK_KP_9 or key == terminal.TK_Y:
            try_move_player(1, -1)
        elif key == terminal.TK_KP_7 or key == terminal.TK_U:
            try_move_player(-1, -1)
        elif key == terminal.TK_KP_3 or key == terminal.TK_N:
            try_move_player(1, 1)
        elif key == terminal.TK_KP_1 or key == terminal.TK_B:
            try_move_player(-1, 1)
        # others
        elif key == terminal.TK_G:
            get_item(World.fetch('player'))
        elif key == terminal.TK_I:
            return States.SHOW_INVENTORY
        elif key == terminal.TK_D:
            return States.SHOW_DROP_ITEM
        elif key == terminal.TK_C:
            Interface.show_character_sheet()
        elif key == terminal.TK_SPACE:
            next_lvl = try_next_level()
            if next_lvl == NextLevelResult.NEXT_FLOOR:
                return States.NEXT_LEVEL
            elif next_lvl == NextLevelResult.EXIT_DUNGEON:
                return States.VICTORY
        elif key == terminal.TK_KP_5 or key == terminal.TK_Z:
            return States.PLAYER_TURN

        elif key == terminal.TK_ESCAPE:
            return States.SAVE_GAME
        elif key == terminal.TK_CLOSE:
            terminal.close()
        else:
            return States.AWAITING_INPUT
        return States.PLAYER_TURN
    return States.AWAITING_INPUT


def targeting_input(item, mouse_coords, valid_target=False):
    cancel = False
    if terminal.has_input():
        logs = World.fetch('logs')
        key = terminal.read()
        if key == terminal.TK_ESCAPE:
            logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_OK}]{Texts.get_text("YOU_CHANGE_MIND")}[/color]')
            cancel = True
        elif key == terminal.TK_MOUSE_LEFT:
            if valid_target and item:
                return ItemMenuResult.SELECTED, item, mouse_coords
            logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]{Texts.get_text("NOTHING_TO_TARGET")}[/color]')
            cancel = True

    if cancel:
        World.remove_component(TargetingComponent, World.fetch('player'))
        return ItemMenuResult.CANCEL, None, None
    return ItemMenuResult.NO_RESPONSE, None, None


def any_input_for_quit():
    if terminal.has_input():
        key = terminal.read()
        if key != terminal.TK_MOUSE_MOVE:
            return ItemMenuResult.SELECTED
    return ItemMenuResult.NO_RESPONSE


def inventory_input(item_list):
    if terminal.has_input():
        key = terminal.read()
        if key == terminal.TK_ESCAPE:
            return ItemMenuResult.CANCEL, None
        else:
            index = terminal.state(terminal.TK_CHAR) - ord('a')
            if 0 <= index < len(item_list):
                return ItemMenuResult.SELECTED, item_list[index]
            return ItemMenuResult.NO_RESPONSE, None
    return ItemMenuResult.NO_RESPONSE, None


def main_menu_input():
    if terminal.has_input():
        key = terminal.read()
        index = terminal.state(terminal.TK_CHAR) - ord('a')
        if key == terminal.TK_ESCAPE or index == 3:
            return MainMenuSelection.QUIT
        elif index == 0:
            return MainMenuSelection.NEWGAME
        elif index == 1:
            return MainMenuSelection.LOAD_GAME
        elif index == 2:
            # change language
            if Texts.get_current_language() == 'fr':
                Texts.set_language('en')
            else:
                Texts.set_language('fr')
            Interface.show_main_menu()
    return MainMenuSelection.NO_RESPONSE


def character_sheet_input():
    if terminal.has_input():
        if terminal.read() == terminal.TK_ESCAPE:
            terminal.clear_area(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
            terminal.refresh()
            Interface.clear()
