from bearlibterminal import terminal

from systems.system import System
from world import World
from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent


class RenderSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(PositionComponent, RenderableComponent)
        if not subjects:
            return

        terminal.layer(2)
        current_map = World.fetch('current_map')
        for entity, (position, render) in subjects:
            idx = current_map.xy_idx(position.x, position.y)
            if current_map.visible_tiles[idx]:
                terminal.printf(position.x, position.y, f'[color={render.fg}]{render.glyph}[/color]')
