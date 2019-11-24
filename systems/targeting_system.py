from bearlibterminal import terminal

from systems.system import System
from systems.ui_system import use_item
from world import World
from components.targeting_component import TargetingComponent
from components.viewshed_component import ViewshedComponent
from components.position_component import PositionComponent
from data.types import Layers, ItemMenuResult
from gmap.utils import distance_to
import config


class TargetingSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(TargetingComponent, ViewshedComponent)
        if not subjects:
            return

        player_pos = World.get_entity_component(World.fetch('player'), PositionComponent)

        for entity, (targeter, viewshed) in subjects:
            terminal.layer(Layers.TOOLTIP.value)
            x = 0
            y = 0
            for row in viewshed.visible_tiles:
                for tile in row:
                    if tile and distance_to(player_pos.x, player_pos.y, x, y) < targeter.range:
                        terminal.printf(x, y, f'[color=red]+[/color]')
                    x += 1
                y += 1
                x = 0

            if terminal.has_input():
                World.remove_component(TargetingComponent, entity)


def show_targeting():
    subjects = World.get_components(TargetingComponent, ViewshedComponent)
    if not subjects:
        return

    player_pos = World.get_entity_component(World.fetch('player'), PositionComponent)

    for entity, (targeter, viewshed) in subjects:
        terminal.layer(Layers.BACKGROUND.value)

        mouse_pos_x = terminal.state(terminal.TK_MOUSE_X)
        mouse_pos_y = terminal.state(terminal.TK_MOUSE_Y)
        valid_target = False

        x = 0
        y = 0
        for row in viewshed.visible_tiles:
            for tile in row:
                if tile and distance_to(player_pos.x, player_pos.y, x, y) < targeter.range:
                    if x == mouse_pos_x and y == mouse_pos_y:
                        terminal.printf(x, y, f'[bkcolor=light blue] [/color]')
                        valid_target = True
                    else:
                        terminal.printf(x, y, f'[bkcolor=dark blue] [/color]')
                x += 1
            y += 1
            x = 0

        terminal.refresh()

        cancel = False
        if terminal.has_input():
            logs = World.fetch('logs')
            key = terminal.read()
            if key == terminal.TK_ESCAPE:
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_OK}]You change your mind.[/color]')
                cancel = True
            elif key == terminal.TK_MOUSE_LEFT:
                if valid_target:
                    return ItemMenuResult.SELECTED, targeter.item, (mouse_pos_x, mouse_pos_y)
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]There is nothing to target there.[/color]')
                cancel = True
        if cancel:
            World.remove_component(TargetingComponent, entity)
            return ItemMenuResult.CANCEL, None, None
        return ItemMenuResult.NO_RESPONSE, None, None


def select_target(item_id, target_position):
    use_item(item_id, target_position)
    print(f'target selected with item {item_id} at position {target_position}')
