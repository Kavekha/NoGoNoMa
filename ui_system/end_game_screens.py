from bearlibterminal import terminal
from ui_system.ui_enums import ItemMenuResult
from player_systems.player_input import any_input_for_quit


def show_game_over():
    terminal.printf(15, 15, f'GAME OVER')
    terminal.printf(15, 20, 'Press any Key to go back to Main Menu')

    terminal.refresh()
    return any_input_for_quit()


def show_victory_screen():
    terminal.printf(15, 15, f'VICTORY !!!!')
    terminal.printf(15, 17, f'You escape the dungeon.')
    terminal.printf(15, 20, 'Press any Key to go back to Main Menu')

    terminal.refresh()

    terminal.refresh()
    return any_input_for_quit()
