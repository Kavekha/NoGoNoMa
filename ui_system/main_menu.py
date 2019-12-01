from bearlibterminal import terminal

from ui_system.ui_enums import Layers
from player_systems.player_input import main_menu_input
from texts import Texts


def main_menu():
    terminal.layer(Layers.MENU.value)
    letter_index = ord('a')
    terminal.printf(15, 10, f'[color=yellow]{Texts.get_text("GAME_TITLE")}[/color]')
    terminal.printf(15, 20, f'[color=orange]({chr(letter_index)}) {Texts.get_text("NEW_GAME")}[/color]')
    letter_index += 1
    terminal.printf(15, 22, f'[color=orange]({chr(letter_index)}) {Texts.get_text("LOAD_GAME")}[/color]')
    letter_index += 1
    terminal.printf(15, 24, f'[color=orange]({chr(letter_index)}) {Texts.get_text("QUIT")}[/color]')

    terminal.refresh()

    return main_menu_input()
