from components.equip_components import EquippedComponent
from components.item_components import MeleeWeaponComponent
from systems.inventory_system import drop_item_from_inventory, select_item_from_inventory
from world import World


def get_available_item_actions(item):
    item_weapon = World.get_entity_component(item, MeleeWeaponComponent)
    item_equipped = World.get_entity_component(item, EquippedComponent)

    available_actions = list()
    if item_weapon:
        if item_equipped:
            # equip
            available_actions.append(select_item_from_inventory)
        else:
            # unequip
            available_actions.append(select_item_from_inventory)
    else:
        # use
        available_actions.append(select_item_from_inventory)
    # drop
    available_actions.append(drop_item_from_inventory)

    return available_actions
