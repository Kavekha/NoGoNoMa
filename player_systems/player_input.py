from bearlibterminal import terminal
from player_systems.try_move_player import try_move_player, try_next_level
from systems.inventory_system import get_item
from data.types import States
from world import World


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
        elif key == terminal.TK_SPACE:
            if try_next_level():
                return States.NEXT_LEVEL

        elif key == terminal.TK_ESCAPE:
            return States.SAVE_GAME
        elif key == terminal.TK_CLOSE:
            terminal.close()
        else:
            return States.AWAITING_INPUT
        return States.PLAYER_TURN
    return States.AWAITING_INPUT
