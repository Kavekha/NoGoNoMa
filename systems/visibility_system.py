from systems.system import System
from world import World
from components.position_component import PositionComponent
from components.viewshed_component import ViewshedComponent
from components.player_component import PlayerComponent
import config


class VisibilitySystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(PositionComponent, ViewshedComponent)

        current_map = World.fetch('current_map')
        for entity, (position, viewshed) in subjects:
            viewshed.dirty = False
            viewshed.visible_tiles = []
            if entity == World.fetch('player'):
                # on enregistre les murs comme visibles
                current_map.fov_map.compute_fov(position.x, position.y, viewshed.visible_range, viewshed.light_wall)
            else:
                current_map.fov_map.compute_fov(position.x, position.y, viewshed.visible_range, False)
            viewshed.visible_tiles = current_map.fov_map.fov.copy()

            if World.entity_has_component(entity, PlayerComponent):
                current_map.visible_tiles = [False] * (config.MAP_HEIGHT * config.MAP_WIDTH)
                x = 0
                y = 0
                for row in viewshed.visible_tiles:
                    for tile in row:
                        if tile:
                            idx = current_map.xy_idx(x, y)
                            current_map.revealed_tiles[idx] = True
                            current_map.visible_tiles[idx] = True
                        x += 1
                    y += 1
                    x = 0
