from bearlibterminal import terminal

from systems.system import System
from world import World
from components.combat_stats_component import CombatStatsComponent
from components.player_component import PlayerComponent
from ui_system.ui_enums import Layers
import config
from texts import Texts


class UiSystem(System):
    def update(self, *args, **kwargs):
        # display HP
        subjects = World.get_components(CombatStatsComponent, PlayerComponent)
        if not subjects:
            return

        current_map = World.fetch('current_map')
        terminal.layer(Layers.INTERFACE.value)
        terminal.printf(1, config.UI_STATS_INFO_LINE, f'[color=light grey]{Texts.get_text("DEPTH")}'
                                                      f': {current_map.depth}[/color]')
        for entity, (combat_stats, player) in subjects:
            terminal.printf(20, config.UI_STATS_INFO_LINE, f'[color=light grey]{Texts.get_text("HP")}: '
                                                           f'{combat_stats.hp} / {combat_stats.max_hp}[/color]')

        log = World.fetch('logs')
        y = config.UI_LOG_FIRST_LINE
        for line in log:
            if y < config.SCREEN_HEIGHT:
                terminal.printf(2, y, line)
                y += 1
