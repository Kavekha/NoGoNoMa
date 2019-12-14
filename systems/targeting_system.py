from bearlibterminal import terminal

from systems.inventory_system import use_item
from systems.render_system import render_system
from world import World
from components.targeting_component import TargetingComponent
from components.viewshed_component import ViewshedComponent
from components.position_component import PositionComponent
from ui_system.ui_enums import Layers
from ui_system.interface import Interface, GraphicalModes
from gmap.utils import distance_to
from player_systems.player_input import targeting_input


def show_targeting():
    subjects = World.get_components(TargetingComponent, ViewshedComponent)
    player_pos = World.get_entity_component(World.fetch('player'), PositionComponent)

    for entity, (targeter, viewshed) in subjects:
        mouse_pos_x = terminal.state(terminal.TK_MOUSE_X)
        mouse_pos_y = terminal.state(terminal.TK_MOUSE_Y)
        valid_target = False

        x = 0
        y = 0
        for row in viewshed.visible_tiles:
            for tile in row:
                if tile and distance_to(player_pos.x, player_pos.y, x, y) < targeter.range:
                    if x == mouse_pos_x and y == mouse_pos_y:
                        if Interface.mode == GraphicalModes.ASCII:
                            terminal.layer(Layers.BACKGROUND.value)
                            terminal.printf(x, y, f'[bkcolor=light blue] [/color]')
                        elif Interface.mode == GraphicalModes.TILES:
                            terminal.color('light blue')
                            terminal.put(x, y, Interface.get_code('system/grid.png'))
                        else:
                            print(f'targeting system: graphical mode not implemented.')
                            raise NotImplementedError
                        valid_target = True
                    else:
                        if Interface.mode == GraphicalModes.ASCII:
                            terminal.layer(Layers.BACKGROUND.value)
                            terminal.printf(x, y, f'[bkcolor=dark blue] [/color]')
                        elif Interface.mode == GraphicalModes.TILES:
                            terminal.color('light blue')
                            terminal.put(x, y, Interface.get_code('system/grid.png'))
                        else:
                            print(f'targeting system: graphical mode not implemented.')
                            raise NotImplementedError
                x += 1
            y += 1
            x = 0

        render_system()
        terminal.refresh()

        return targeting_input(targeter.item, (mouse_pos_x, mouse_pos_y), valid_target)


def select_target(item_id, target_position):
    use_item(item_id, target_position)
