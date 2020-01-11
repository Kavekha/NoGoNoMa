from bearlibterminal import terminal

import time

import config
from world import World
from data.load_raws import RawsMaster
from systems.particule_system import cull_dead_particules
from ui_system.interface import Interface
from ui_system.show_menus import show_main_menu
from state import States, State
from tick import tick

MASTER_SEED = 1000


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
    Interface()
    Interface.initialize()

    show_main_menu()
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
