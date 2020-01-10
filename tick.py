from bearlibterminal import terminal

import sys

import config
from world import World
from player_systems.player_input import player_input
from ui_system.draw_tooltip import draw_tooltip
from systems.targeting_system import show_targeting, select_target
from player_systems.player_input import main_menu_input, input_escape_to_quit, inventory_input, option_menu_input, \
    inventory_selected_item_input, yes_no_input
from ui_system.ui_enums import ItemMenuResult, MainMenuSelection, OptionMenuSelection, YesNoResult
from systems.inventory_system import get_items_in_inventory
from ui_system.interface import Interface
from ui_system.show_menus import show_item_screen, show_main_options_menu, show_selected_item_screen, show_main_menu
from ui_system.render_camera import render_map_camera, render_entities_camera, render_debug_map
from state import States
from data.save_and_load import load_game, save_game, has_saved_game
from data.initialize_game import init_game


def tick():
    run_state = World.fetch('state')

    # Menus
    if run_state.current_state == States.MAIN_MENU:
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
            show_main_options_menu()
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

    elif run_state.current_state == States.CONFIRM_QUIT:
        result = yes_no_input()
        if result == YesNoResult.NO:
            # Je ne veux plus quitter
            run_state.change_state(States.AWAITING_INPUT)
            run_render_systems()
        elif result == YesNoResult.YES:
            run_state.change_state(States.SAVE_GAME)
            run_render_systems()

    elif run_state.current_state == States.SAVE_GAME:
        run_state.change_state(States.MAIN_MENU)
        save_game(World)
        World.reset_all()
        show_main_menu()

    elif run_state.current_state == States.OPTION_MENU:
        result = option_menu_input()
        if result == OptionMenuSelection.BACK_TO_MAIN_MENU:
            show_main_menu()
            run_state.change_state(States.MAIN_MENU)

    elif run_state.current_state == States.GAME_OVER:
        result = input_escape_to_quit()
        if result == ItemMenuResult.SELECTED:
            World.reset_all()
            terminal.clear()
            show_main_menu()
            run_state.change_state(States.MAIN_MENU)

    elif run_state.current_state == States.VICTORY:
        result = input_escape_to_quit()
        if result == ItemMenuResult.SELECTED:
            World.reset_all()
            terminal.clear()
            show_main_menu()
            run_state.change_state(States.MAIN_MENU)

    elif run_state.current_state == States.CHARACTER_SHEET:
        result = input_escape_to_quit()
        if result == ItemMenuResult.SELECTED:
            run_state.change_state(States.AWAITING_INPUT)
            run_game_systems()

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
        run_game_systems()
        run_render_systems()

    elif run_state.current_state == States.AWAITING_INPUT:
        run_state.change_state(player_input())
        draw_tooltip()

    elif run_state.current_state == States.TICKING:
        run_game_systems()
        if run_state.current_state == States.AWAITING_INPUT:
            run_render_systems()

    # In game menus
    elif run_state.current_state == States.SHOW_INVENTORY:
        items_in_backpack = get_items_in_inventory(World.fetch('player'))
        result, new_state, item = inventory_input(items_in_backpack)
        if result == ItemMenuResult.CANCEL:
            run_render_systems()
            run_state.change_state(States.AWAITING_INPUT)
        elif result == ItemMenuResult.SELECTED:
            run_state.args = item
            run_state.change_state(new_state)
            run_game_systems()
            show_selected_item_screen(item)

    # menu inventory with item selected
    elif run_state.current_state == States.SHOW_SELECTED_ITEM_MENU:
        chosen_item = run_state.args
        result, action = inventory_selected_item_input(chosen_item)
        if result == ItemMenuResult.DESELECT:
            run_game_systems()
            run_state.args = None
            run_state.change_state(States.SHOW_INVENTORY)
            show_item_screen()
        elif result == ItemMenuResult.ACTION:
            print(f'action is : {action}')
            new_state = action(chosen_item)
            run_state.change_state(new_state)
            run_render_systems()

    elif run_state.current_state == States.SHOW_TARGETING:
        result, item, target_pos = show_targeting()
        if result == ItemMenuResult.CANCEL:
            run_state.change_state(States.TICKING)
        elif result == ItemMenuResult.SELECTED:
            select_target(item, target_pos)
            run_state.change_state(States.TICKING)

    # Mecanisms
    elif run_state.current_state == States.NEXT_LEVEL:
        run_state.go_next_level()
        run_state.change_state(States.PRE_RUN)
    else:
        run_game_systems()
        run_state.change_state(States.TICKING)


def run_game_systems():
    World.update()


def run_render_systems():
    terminal.clear()
    World.update()
    render_map_camera()
    render_entities_camera()
    draw_tooltip()
    terminal.refresh()
