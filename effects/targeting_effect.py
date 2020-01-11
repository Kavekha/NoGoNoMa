from world import World
from components.position_components import PositionComponent


def entity_position(entity):
    entity_pos = World.get_entity_component(entity, PositionComponent)
    if entity_pos:
        current_map = World.fetch('current_map')
        return current_map.xy_idx(entity_pos.x, entity_pos.y)
