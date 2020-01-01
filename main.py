from bearlibterminal import terminal

import sys
import time

import config
from world import World
from data.load_raws import RawsMaster
from player_systems.player_input import player_input
from ui_system.draw_tooltip import draw_tooltip
from systems.targeting_system import show_targeting, select_target
from systems.inventory_system import select_item_from_inventory, drop_item_from_inventory
from player_systems.player_input import main_menu_input, input_escape_to_quit, inventory_input, option_menu_input
from ui_system.ui_enums import ItemMenuResult, MainMenuSelection, OptionMenuSelection
from systems.inventory_system import get_items_in_user_backpack
from systems.particule_system import cull_dead_particules
from ui_system.interface import Interface
from ui_system.menus import show_main_menu, show_character_sheet, show_game_over_screen, show_victory_screen, \
    show_item_screen, show_option_menu
from ui_system.render_camera import render_map_camera, render_entities_camera, render_debug_map
from state import States, State
from data.save_and_load import load_game, save_game, has_saved_game
from data.initialize_game import init_game
from texts import Texts


MASTER_SEED = 1000


def tick():
    run_state = World.fetch('state')

    # Menus
    if run_state.current_state == States.MAIN_MENU:
        show_main_menu()
        result = main_menu_input()
        if result == MainMenuSelection.NEWGAME:
            if config.SHOW_MAPGEN_VISUALIZER:
                run_state.change_state(States.MAP_GENERATION)
            else:
                run_state.change_state(States.PRE_RUN)
            World.reset_all()
            init_game()  # MASTER_SEED)
        elif result == MainMenuSelection.LOAD_GAME:
            run_state.change_state(States.LOAD_GAME)
        elif result == MainMenuSelection.QUIT:
            sys.exit()
        elif result == MainMenuSelection.OPTION:
            terminal.clear()
            run_state.change_state(States.OPTION_MENU)

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

    elif run_state.current_state == States.OPTION_MENU:
        show_option_menu()
        result = option_menu_input()
        if result == OptionMenuSelection.BACK_TO_MAIN_MENU:
            terminal.clear()
            run_state.change_state(States.MAIN_MENU)

    elif run_state.current_state == States.GAME_OVER:
        terminal.clear()
        show_game_over_screen()
        result = input_escape_to_quit()
        if result == ItemMenuResult.SELECTED:
            World.reset_all()
            terminal.clear()
            run_state.change_state(States.MAIN_MENU)

    elif run_state.current_state == States.VICTORY:
        terminal.clear()
        show_victory_screen()
        result = input_escape_to_quit()
        if result == ItemMenuResult.SELECTED:
            World.reset_all()
            terminal.clear()
            run_state.change_state(States.MAIN_MENU)

    elif run_state.current_state == States.CHARACTER_SHEET:
        show_character_sheet()
        result = input_escape_to_quit()
        if result == ItemMenuResult.SELECTED:
            run_state.change_state(States.AWAITING_INPUT)
            run_systems()

    # map gen
    elif run_state.current_state == States.MAP_GENERATION:
        Interface.set_zoom(1)
        if not config.SHOW_MAPGEN_VISUALIZER:
            run_state.change_state(States.PRE_RUN)
        else:
            terminal.clear()
            render_debug_map(run_state.mapgen_history[run_state.mapgen_index])
            run_state.mapgen_timer += 1
            if run_state.mapgen_timer > config.MAPGEN_VISUALIZER_TIMER:
                run_state.mapgen_timer = 0
                run_state.mapgen_index += 1
                if run_state.mapgen_index >= len(run_state.mapgen_history):
                    run_state.change_state(States.PRE_RUN)
            terminal.refresh()

    # Game State
    elif run_state.current_state == States.PRE_RUN:
        run_state.change_state(States.AWAITING_INPUT)
        run_systems()

    elif run_state.current_state == States.AWAITING_INPUT:
        run_state.change_state(player_input())
        draw_tooltip()

    elif run_state.current_state == States.PLAYER_TURN:
        run_systems()
        if run_state.current_state == States.PLAYER_TURN:
            run_state.change_state(States.MONSTER_TURN)

    elif run_state.current_state == States.MONSTER_TURN:
        run_systems()
        if run_state.current_state == States.MONSTER_TURN:
            run_state.change_state(States.AWAITING_INPUT)

    # In game menus
    elif run_state.current_state == States.SHOW_INVENTORY:
        show_item_screen(f'[color=yellow] {Texts.get_text("INVENTORY")} [/color]')
        items_in_backpack = get_items_in_user_backpack(World.fetch('player'))
        result, item = inventory_input(items_in_backpack)
        if result == ItemMenuResult.CANCEL:
            run_systems()
            run_state.change_state(States.AWAITING_INPUT)
        elif result == ItemMenuResult.SELECTED:
            new_state = select_item_from_inventory(item)
            run_systems()
            run_state.change_state(new_state)

    elif run_state.current_state == States.SHOW_DROP_ITEM:
        show_item_screen(f'[color=yellow] {Texts.get_text("DROP_WHICH_ITEM")}[/color]')
        items_in_backpack = get_items_in_user_backpack(World.fetch('player'))
        result, item = inventory_input(items_in_backpack)
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
    render_map_camera()
    render_entities_camera()
    draw_tooltip()
    terminal.refresh()


def main():
    # Word is the main system.
    terminal.open()
    terminal.set(f'window: title={config.TITLE}, size={config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}')
    terminal.set(f'font: {config.FONT}')
    terminal.set("input.filter={keyboard, mouse+}")
    terminal.refresh()

    # load raws
    RawsMaster()
    RawsMaster.load_raws()

    # Interface
    interface = Interface()
    Interface.initialize()

    run_state = State(States.MAIN_MENU)
    World.insert('state', run_state)

    FPS = 200    #config.FPS

    while True:
        start_time = time.perf_counter()  # limit fps
        tick()
        cull_dead_particules(start_time)
        delta_time = (time.perf_counter() - start_time) * 1000
        terminal.delay(max(int(1000.0 / FPS - delta_time), 0))


if __name__ == '__main__':
    main()
