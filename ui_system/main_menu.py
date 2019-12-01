from bearlibterminal import terminal

from ui_system.ui_enums import Layers, MainMenuSelection
from player_systems.player_input import main_menu_input


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

    return main_menu_input()
