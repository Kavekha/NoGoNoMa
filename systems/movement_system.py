from world import World
from systems.system import System
from player_systems.initiative_costs_mecanisms import calculate_move_cost
from components.position_components import PositionComponent, ApplyMoveComponent, EntityMovedComponent
from components.blocktile_component import BlockTileComponent
from components.viewshed_component import ViewshedComponent
from components.character_components import AutopickupComponent
from systems.inventory_system import get_item


class MovementSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(PositionComponent, ApplyMoveComponent)
        current_map = World.fetch('current_map')

        for entity, (position, move) in subjects:
            start_idx = current_map.xy_idx(position.x, position.y)
            dest_idx = move.dest_idx

            # Est ce qu'il "bloque" la tile en se deplacant?
            blocking = World.get_entity_component(entity, BlockTileComponent)
            if blocking:
                current_map.blocked_tiles[start_idx] = False
                current_map.blocked_tiles[dest_idx] = True

            # movement
            position.x, position.y = current_map.index_to_point2d(dest_idx)

            viewshed = World.get_entity_component(entity, ViewshedComponent)
            if viewshed:
                viewshed.dirty = True

            # autopickup
            if World.get_entity_component(entity, AutopickupComponent):
                get_item(entity)

            World.add_component(EntityMovedComponent(), entity)
            World.add_component(calculate_move_cost(entity), entity)

        World.remove_component_for_all_entities(ApplyMoveComponent)
