from bearlibterminal import terminal

from systems.system import System
from world import World
from components.targeting_component import TargetingComponent
from components.viewshed_component import ViewshedComponent
from components.position_component import PositionComponent
from data.types import Layers, ItemMenuResult
from gmap.utils import distance_to


class TargetingSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(TargetingComponent, ViewshedComponent)
        if not subjects:
            return

        player_pos = World.get_entity_component(World.fetch('player'), PositionComponent)

        for entity, (targeter, viewshed) in subjects:
            print(f'entity targeting is {entity}')
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
                print(f'input, let bail')
                World.remove_component(TargetingComponent, entity)




def show_targeting():

    subjects = World.get_components(TargetingComponent, ViewshedComponent)
    if not subjects:
        return

    player_pos = World.get_entity_component(World.fetch('player'), PositionComponent)

    for entity, (targeter, viewshed) in subjects:
        print(f'sho targeting')
        print(f'entity targeting is {entity}')
        terminal.layer(Layers.TOOLTIP.value)
        x = 0
        y = 0
        for row in viewshed.visible_tiles:
            for tile in row:
                if tile and distance_to(player_pos.x, player_pos.y, x, y) < targeter.range:
                    terminal.printf(x, y, f'[color=dark blue]o[/color]')
                x += 1
            y += 1
            x = 0

        terminal.refresh()

        if terminal.has_input():
            key = terminal.read()
            if key == terminal.TK_ESCAPE:
                World.remove_component(TargetingComponent, entity)
                return ItemMenuResult.CANCEL
        return ItemMenuResult.NO_RESPONSE
