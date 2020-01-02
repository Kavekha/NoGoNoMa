from bearlibterminal import terminal

from systems.system import System
from player_systems.game_system import xp_for_next_level
from world import World
from components.pools_component import Pools
from ui_system.ui_enums import Layers
import config
from texts import Texts
from ui_system.interface import Interface, GraphicalModes
from ui_system.render_functions import render_bar, print_shadow


class UiSystem(System):
    def update(self, *args, **kwargs):
        player = World.fetch('player')
        player_pool = World.get_entity_component(player, Pools)
        current_map = World.fetch('current_map')

        info_to_display = {
            'depth': current_map.depth,
            'player_hp': player_pool.hit_points.current,
            'player_max_hp': player_pool.hit_points.max,
            'player_current_xp': player_pool.xp,
            'player_next_level_xp': xp_for_next_level(player_pool.level)
        }

        if Interface.mode == GraphicalModes.ASCII:
            self.draw_ui_ascii(info_to_display)
        elif Interface.mode == GraphicalModes.TILES:
            self.draw_ui_tiles(info_to_display)
        else:
            print(f'Graphical mode is {Interface.mode}, no UI support for this mode.')
            raise NotImplementedError

    def draw_ui_ascii(self, info_to_display):
        terminal.layer(Layers.INTERFACE.value)
        # map name
        map_name = World.fetch('current_map').name
        map_name = f'{Texts.get_text(map_name)  + " - " + str(info_to_display["depth"])}'
        center_x = (Interface.screen_width - len(map_name)) // 2
        map_name = f'[color=yellow]{map_name}[/color]'
        terminal.printf(center_x, Interface.ui_model.ui_map_name.start_y,
                        f'[color=yellow]{map_name}[/color]')

        terminal.printf(20, config.UI_STATS_INFO_LINE, f'[color=light grey]{Texts.get_text("HP")}: '
                                                       f'{info_to_display.get("player_hp", "??")} / '
                                                       f'{info_to_display.get("player_max_hp", "??")}[/color]')
        terminal.printf(45, config.UI_STATS_INFO_LINE, f'[color=light grey]{Texts.get_text("XP")}: '
                                                       f'{info_to_display.get("player_current_xp", "??")} / '
                                                       f'{info_to_display.get("player_next_level_xp", "??")}[/color]')

        logs = World.fetch('logs')
        y = config.UI_LOG_FIRST_LINE
        for line in logs:
            if y < config.SCREEN_HEIGHT:
                terminal.printf(2, y, line)
                y += 1

    def draw_ui_tiles(self, info_to_display):
        terminal.layer(Layers.INTERFACE.value)
        # map name
        map_name = World.fetch('current_map').name
        map_name = f'{Texts.get_text(map_name)  + " - " + str(info_to_display["depth"])}'
        center_x = (Interface.screen_width - len(map_name)) // 2
        map_name = f'[color=yellow]{map_name}[/color]'
        terminal.printf(center_x, Interface.ui_model.ui_map_name.start_y,
                        f'[color=yellow]{map_name}[/color]')

        # HP
        render_bar(Interface.ui_model.ui_player_bars.start_x,
                   Interface.ui_model.ui_player_bars.start_y,
                   config.UI_HP_BAR_WIDTH + min(info_to_display.get("player_max_hp", 0) // 2,
                                                config.UI_HP_BAR_WIDTH * 3),
                   Texts.get_text("HP"),
                   info_to_display.get("player_hp", 0),
                   info_to_display.get("player_max_hp", 0),
                   config.COLOR_HP_BAR_VALUE,
                   config.COLOR_HP_BAR_BACKGROUND,
                   config.COLOR_TEXT_HP_BAR)

        # XP
        render_bar(Interface.ui_model.ui_player_bars.start_x,
                   Interface.ui_model.ui_player_bars.start_y + 1,
                   config.UI_XP_BAR_WIDTH + min(info_to_display.get("player_next_level_xp", 0) // 10,
                                                config.UI_XP_BAR_WIDTH * 3),
                   Texts.get_text("XP"),
                   info_to_display.get("player_current_xp", 0),
                   info_to_display.get("player_next_level_xp", 0),
                   config.COLOR_XP_BAR_VALUE,
                   config.COLOR_XP_BAR_BACKGROUND,
                   config.COLOR_TEXT_XP_BAR)

        log = World.fetch('logs')
        y = Interface.ui_model.ui_logs.start_y
        for line in log:
            if y < config.SCREEN_HEIGHT:
                print_shadow(2, y, line)
                y += 1
