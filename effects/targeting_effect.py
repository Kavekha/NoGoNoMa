from itertools import product as it_product

from world import World
from components.position_components import PositionComponent
from components.item_components import InBackPackComponent
from components.equip_components import EquippedComponent


def get_aoe_tiles(target, aoe_radius):
    blast_tiles_idx = list()
    current_map = World.fetch('current_map')

    target_x, target_y = target
    # idx = current_map.xy_idx(target_x, target_y)
    radius = aoe_radius // 2

    for x, y in it_product(range(- radius, radius + 1), range(- radius, radius + 1)):
        radius_x = target_x + x
        radius_y = target_y + y
        new_idx = current_map.xy_idx(radius_x, radius_y)
        if not current_map.out_of_bound(new_idx):
            blast_tiles_idx.append(new_idx)

    return blast_tiles_idx


def entity_position(entity):
    entity_pos = World.get_entity_component(entity, PositionComponent)
    if entity_pos:
        current_map = World.fetch('current_map')
        return current_map.xy_idx(entity_pos.x, entity_pos.y)


def find_item_position(entity):
    current_map = World.fetch('current_map')

    # it has a position
    pos = World.get_entity_component(entity, PositionComponent)
    if pos:
        return current_map.xy_idx(pos.x, pos.y)

    # it is carried
    carried = World.get_entity_component(entity, InBackPackComponent)
    if carried:
        pos = World.get_entity_component(carried.owner, PositionComponent)
        if pos:
            return current_map.xy_idx(pos.x, pos.y)

    # equipped?
    equipped = World.get_entity_component(entity, EquippedComponent)
    if equipped:
        pos = World.get_entity_component(equipped.owner, PositionComponent)
        if pos:
            return current_map.xy_idx(pos.x, pos.y)

    # no idea
    return None