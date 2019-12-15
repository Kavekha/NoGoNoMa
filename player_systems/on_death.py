from state import States
from data.save_and_load import save_game
from world import World
from texts import Texts
import config


def on_player_death():
    logs = World.fetch('logs')
    logs.appendleft(f'[color={config.COLOR_DEADLY_INFO}]{Texts.get_text("YOU_ARE_DEAD")}[/color]')
    save_game(World)
    run_state = World.fetch('state')
    run_state.change_state(States.GAME_OVER)
