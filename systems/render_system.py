from bearlibterminal import terminal


from world import World
from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent
from ui_system.interface import Interface, GraphicalModes
from gmap.utils import xy_idx


def render_system():
    subjects = World.get_components(PositionComponent, RenderableComponent)
    current_map = World.fetch('current_map')

    if Interface.mode == GraphicalModes.ASCII:
        render_entities_ascii(subjects, current_map)
    elif Interface.mode == GraphicalModes.TILES:
        render_entities_tiles(subjects, current_map)
    else:
        print(f'render system : graphical mode {Interface.mode} not supported')
        raise NotImplementedError


def render_entities_ascii(subjects, current_map):
    for entity, (position, render) in subjects:
        idx = xy_idx(position.x, position.y)
        if current_map.visible_tiles[idx]:
            terminal.layer(render.render_order.value)
            terminal.printf(position.x, position.y, f'[color={render.fg}]{render.glyph}[/color]')


def render_entities_tiles(subjects, current_map):
    for entity, (position, render) in subjects:
        idx = xy_idx(position.x, position.y)
        if current_map.visible_tiles[idx]:
            terminal.layer(render.render_order.value)
            terminal.color(render.fg)
            terminal.put(position.x, position.y, Interface.get_code(render.sprite))
