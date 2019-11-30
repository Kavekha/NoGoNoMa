# http://bfnightly.bracketproductions.com/rustbook/chapter_9.html

from bearlibterminal import terminal
from collections import deque
from random import seed
import sys
import time

import config
from world import World
from player_systems.player_input import player_input
from systems.render_system import render_system
from systems.visibility_system import VisibilitySystem
from systems.monster_ai_system import MonsterAi
from systems.map_indexing_system import MapIndexingSystem
from systems.melee_combat_system import MeleeCombatSystem
from systems.damage_system import DamageSystem
from systems.death_system import DeathSystem
from systems.ui_system import UiSystem, draw_tooltip, show_inventory, select_item_from_inventory, drop_item_menu, \
    drop_item_from_inventory
from systems.targeting_system import show_targeting, select_target
from systems.inventory_system import ItemCollectionSystem, ItemDropSystem
from systems.item_use_system import ItemUseSystem
from menus.main_menu import main_menu
from gmap.map_creation import Gmap
from gmap.draw_map import draw_map
from data.types import States, ItemMenuResult, MainMenuSelection
from state import State
from data.save_and_load import load_game, save_game, has_saved_game
from gmap.spawner import spawn_world, spawn_player


MASTER_SEED = 1000


def tick():
    run_state = World.fetch('state')
    if run_state.current_state == States.MAIN_MENU:
        result = main_menu()
        if result == MainMenuSelection.NEWGAME:
            World.reset_all()
            init_game(MASTER_SEED)
            run_state.change_state(States.PRE_RUN)
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
            print(f'no save file')
            run_state.change_state(States.MAIN_MENU)

    elif run_state.current_state == States.SAVE_GAME:
        save_game(World)
        World.reset_all()
        terminal.clear()
        run_state.change_state(States.MAIN_MENU)

    elif run_state.current_state == States.PRE_RUN:
        run_systems()
        run_state.change_state(States.AWAITING_INPUT)

    elif run_state.current_state == States.AWAITING_INPUT:
        run_state.change_state(player_input())
        draw_tooltip()

    elif run_state.current_state == States.PLAYER_TURN:
        run_systems()
        run_state.change_state(States.MONSTER_TURN)

    elif run_state.current_state == States.MONSTER_TURN:
        run_systems()
        run_state.change_state(States.AWAITING_INPUT)

    elif run_state.current_state == States.SHOW_INVENTORY:
        result, item = show_inventory(World.fetch('player'))
        if result == ItemMenuResult.CANCEL:
            run_state.change_state(States.AWAITING_INPUT)
            run_systems()
        elif result == ItemMenuResult.SELECTED:
            new_state = select_item_from_inventory(item)
            run_systems()
            run_state.change_state(new_state)

    elif run_state.current_state == States.SHOW_DROP_ITEM:
        result, item, target_pos = drop_item_menu(World.fetch('player'))
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

    elif run_state.current_state == States.NEXT_LEVEL:
        run_state.go_next_level()
        run_state.change_state(States.PRE_RUN)


def run_systems():
    terminal.clear()
    World.update()
    draw_map()
    render_system()
    draw_tooltip()
    terminal.refresh()


def render_entities():
    render_system()


def init_game(master_seed):
    seed(master_seed)
    World.insert('seed', master_seed)

    # create systems.
    visibility_system = VisibilitySystem()
    World.add_system(visibility_system)
    monster_ai_system = MonsterAi()
    World.add_system(monster_ai_system)
    map_indexing_system = MapIndexingSystem()
    World.add_system(map_indexing_system)
    melee_combat_system = MeleeCombatSystem()
    World.add_system(melee_combat_system)
    damage_system = DamageSystem()
    World.add_system(damage_system)
    death_system = DeathSystem()
    World.add_system(death_system)
    ui_system = UiSystem()
    World.add_system(ui_system)
    inventory_system = ItemCollectionSystem()
    World.add_system(inventory_system)
    drop_system = ItemDropSystem()
    World.add_system(drop_system)
    item_use_system = ItemUseSystem()
    World.add_system(item_use_system)

    # create map
    current_map = Gmap(1)
    World.insert('current_map', current_map)

    # create entities in current_map
    spawn_world(current_map)

    # add player position to ressources
    x, y = current_map.rooms[0].center()
    player = spawn_player(x, y)
    World.insert('player', player)

    # add logs
    log_entry = deque()
    log_entry.append("Welcome to RuToPy Roguelike!")
    World.insert('logs', log_entry)


def main():
    # Word is the main system.

    terminal.open()
    terminal.set(f'window: title={config.TITLE}, size={config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}')
    terminal.set(f'font: {config.FONT}')
    terminal.set("input.filter={keyboard, mouse+}")
    terminal.refresh()

    run_state = State(States.MAIN_MENU)
    World.insert('state', run_state)

    iteration = 0
    FPS = 100
    while True:
        start_time = time.perf_counter()  # limit fps
        tick()
        iteration += 1
        delta_time = (time.perf_counter() - start_time) * 1000
        terminal.delay(max(int(1000.0 / FPS - delta_time), 0))


if __name__ == '__main__':
    main()
