# http://bfnightly.bracketproductions.com/rustbook/chapter_9.html

from bearlibterminal import terminal
from collections import deque
from random import seed

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

from gmap.map_creation import Gmap
from gmap.draw_map import draw_map
from data.types import States, State, ItemMenuResult
from gmap.spawner import spawn_world, spawn_player


def tick():

    run_state = World.fetch('state')
    if run_state.current_state == States.PRE_RUN:
        run_systems()
        run_state.change_state(States.AWAITING_INPUT)

    elif run_state.current_state == States.AWAITING_INPUT:
        run_state.change_state(player_input(run_state))
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


def run_systems():
    terminal.clear()
    World.update()
    draw_map()
    render_system()
    draw_tooltip()
    terminal.refresh()


def render_entities():
    render_system()


def main(main_seed):
    # Word is the main system.

    # create first seed
    seed(main_seed)
    World.insert('seed', main_seed)

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
    current_map = Gmap()
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

    # Add State to World
    state = State(States.PRE_RUN)
    World.insert('state', state)

    terminal.open()
    terminal.set(f'window: title={config.TITLE}, size={config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}')
    terminal.set(f'font: {config.FONT}')
    terminal.set("input.filter={keyboard, mouse+}")
    terminal.refresh()

    while True:
        tick()


if __name__ == '__main__':
    main_seed = 10000
    main(main_seed)
