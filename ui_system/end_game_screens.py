from bearlibterminal import terminal

from texts import Texts
from player_systems.player_input import any_input_for_quit


def show_game_over():
    terminal.printf(15, 15, f'{Texts.get_text("GAME_OVER")}')
    terminal.printf(15, 20, f'{Texts.get_text("PRESS_ANY_KEY")}')

    terminal.refresh()
    return any_input_for_quit()


def show_victory_screen():
    terminal.printf(15, 15, f'{Texts.get_text("VICTORY")}')
    terminal.printf(15, 17, f'{Texts.get_text("YOU_ESCAPE_DUNGEON")}')
    terminal.printf(15, 20, f'{Texts.get_text("PRESS_ANY_KEY")}')

    terminal.refresh()

    terminal.refresh()
    return any_input_for_quit()
