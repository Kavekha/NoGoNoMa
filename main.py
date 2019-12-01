from bearlibterminal import terminal

import sys
import time

import config
from world import World
from player_systems.player_input import player_input
from systems.render_system import render_system
from ui_system.end_game_screens import show_game_over, show_victory_screen
from ui_system.ui_inventory import show_inventory,drop_item_menu
from ui_system.draw_tooltip import draw_tooltip
from systems.targeting_system import show_targeting, select_target
from systems.inventory_system import  select_item_from_inventory, drop_item_from_inventory
from ui_system.main_menu import main_menu
from gmap.draw_map import draw_map
from ui_system.ui_enums import ItemMenuResult, MainMenuSelection
from state import States, State
from data.save_and_load import load_game, save_game, has_saved_game
from data.initialize_game import init_game


MASTER_SEED = 1000


def tick():
    run_state = World.fetch('state')

    # Menus
    if run_state.current_state == States.MAIN_MENU:
        result = main_menu()
        if result == MainMenuSelection.NEWGAME:
            run_state.change_state(States.PRE_RUN)
            World.reset_all()
            init_game(MASTER_SEED)
        elif result == MainMenuSelection.LOAD_GAME:
            run_state.change_state(States.LOAD_GAME)
        elif result == MainMenuSelection.QUIT:
            sys.exit()

    elif run_state.current_state == States.LOAD_GAME:
        if has_saved_game():
            data_file = load_game()
            World.reload_data(data_file)
            run_state.change_state(States.PRE_RUN)
            World.insert('state', run_state)
        else:
            print(f'no save file')  # TODO: Box to inform the player
            run_state.change_state(States.MAIN_MENU)

    elif run_state.current_state == States.SAVE_GAME:
        run_state.change_state(States.MAIN_MENU)
        save_game(World)
        World.reset_all()
        terminal.clear()

    elif run_state.current_state == States.GAME_OVER:
        terminal.clear()
        result = show_game_over()
        if result == ItemMenuResult.SELECTED:
            World.reset_all()
            terminal.clear()
            run_state.change_state(States.MAIN_MENU)

    elif run_state.current_state == States.VICTORY:
        terminal.clear()
        result = show_victory_screen()
        if result == ItemMenuResult.SELECTED:
            World.reset_all()
            terminal.clear()
            run_state.change_state(States.MAIN_MENU)

    # Game State
    elif run_state.current_state == States.PRE_RUN:
        run_state.change_state(States.AWAITING_INPUT)
        run_systems()

    elif run_state.current_state == States.AWAITING_INPUT:
        run_state.change_state(player_input())
        draw_tooltip()

    elif run_state.current_state == States.PLAYER_TURN:
        run_state.change_state(States.MONSTER_TURN)
        run_systems()

    elif run_state.current_state == States.MONSTER_TURN:
        run_state.change_state(States.AWAITING_INPUT)
        run_systems()

    # In game menus
    elif run_state.current_state == States.SHOW_INVENTORY:
        result, item = show_inventory(World.fetch('player'))
        if result == ItemMenuResult.CANCEL:
            run_systems()
            run_state.change_state(States.AWAITING_INPUT)
        elif result == ItemMenuResult.SELECTED:
            new_state = select_item_from_inventory(item)
            run_systems()
            run_state.change_state(new_state)

    elif run_state.current_state == States.SHOW_DROP_ITEM:
        result, item = drop_item_menu(World.fetch('player'))
        if result == ItemMenuResult.CANCEL:
            run_state.change_state(States.AWAITING_INPUT)
            run_systems()
        elif result == ItemMenuResult.SELECTED:
            drop_item_from_inventory(item)
            run_state.change_state(States.PLAYER_TURN)

    elif run_state.current_state == States.SHOW_TARGETING:
        result, item, target_pos = show_targeting()
        if result == ItemMenuResult.CANCEL:
            run_state.change_state(States.PLAYER_TURN)
        elif result == ItemMenuResult.SELECTED:
            select_target(item, target_pos)
            run_state.change_state(States.PLAYER_TURN)

    # Mecanisms
    elif run_state.current_state == States.NEXT_LEVEL:
        run_state.go_next_level()
        run_state.change_state(States.PRE_RUN)


def run_systems():
    print(f'--- run systems ---')
    terminal.clear()
    World.update()
    draw_map()
    render_system()
    draw_tooltip()
    terminal.refresh()


def main():
    # Word is the main system.
    terminal.open()
    terminal.set(f'window: title={config.TITLE}, size={config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}')
    terminal.set(f'font: {config.FONT}')
    terminal.set("input.filter={keyboard, mouse+}")
    terminal.refresh()

    run_state = State(States.MAIN_MENU)
    World.insert('state', run_state)

    FPS = config.FPS

    while True:
        start_time = time.perf_counter()  # limit fps
        tick()
        delta_time = (time.perf_counter() - start_time) * 1000
        terminal.delay(max(int(1000.0 / FPS - delta_time), 0))


if __name__ == '__main__':
    main()
