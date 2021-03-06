from systems.system import System
from world import World
from components.position_components import PositionComponent
from components.blocktile_component import BlockTileComponent


class MapIndexingSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(PositionComponent)
        if not subjects:
            return

        current_map = World.fetch('current_map')
        current_map.populate_blocked()
        current_map.clear_content_index()

        for entity, (position, *args) in subjects:
            idx = current_map.xy_idx(position.x, position.y)

            if World.get_entity_component(entity, BlockTileComponent):
                current_map.blocked_tiles[idx] = True

            # Add the entity in the [] of this tile in tile content
            if not current_map.tile_content[idx]:
                current_map.tile_content[idx] = []
            current_map.tile_content[idx].append(entity)
