from bearlibterminal import terminal

from systems.system import System
from world import World
from components.pools_component import Pools
from components.player_component import PlayerComponent
from ui_system.ui_enums import Layers
import config
from texts import Texts


class UiSystem(System):
    def update(self, *args, **kwargs):
        # display HP
        subjects = World.get_components(Pools, PlayerComponent)
        if not subjects:
            return

        current_map = World.fetch('current_map')
        terminal.layer(Layers.INTERFACE.value)
        terminal.printf(1, config.UI_STATS_INFO_LINE, f'[color=light grey]{Texts.get_text("DEPTH")}'
                                                      f': {current_map.depth}[/color]')
        for entity, (pools, player) in subjects:
            terminal.printf(20, config.UI_STATS_INFO_LINE, f'[color=light grey]{Texts.get_text("HP")}: '
                                                           f'{pools.hit_points.current} / {pools.hit_points.max}[/color]')

        log = World.fetch('logs')
        y = config.UI_LOG_FIRST_LINE
        for line in log:
            if y < config.SCREEN_HEIGHT:
                terminal.printf(2, y, line)
                y += 1
