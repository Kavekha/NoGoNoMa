from bearlibterminal import terminal

from data.types import MainMenuSelection, Layers


def main_menu():
    terminal.layer(Layers.MENU.value)
    letter_index = ord('a')
    terminal.printf(15, 10, f'[color=yellow]NoGo NoMa[/color]')
    terminal.printf(15, 20, f'[color=orange]({chr(letter_index)}) New Game[/color]')
    letter_index += 1
    terminal.printf(15, 22, f'[color=orange]({chr(letter_index)}) Load game[/color]')
    letter_index += 1
    terminal.printf(15, 24, f'[color=orange]({chr(letter_index)}) Quit[/color]')

    terminal.refresh()

    if terminal.has_input():
        key = terminal.read()
        index = terminal.state(terminal.TK_CHAR) - ord('a')
        if key == terminal.TK_ESCAPE or index == 2:
            return MainMenuSelection.QUIT
        elif index == 0:
            return MainMenuSelection.NEWGAME
        elif index == 1:
            return MainMenuSelection.LOAD_GAME
    return MainMenuSelection.NO_RESPONSE
