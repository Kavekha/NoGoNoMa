from components.item_components import MeleeWeaponComponent
from world import World

from components.intent_components import WantsToPickUpComponent
from components.position_components import PositionComponent
from components.item_components import ItemComponent, InBackPackComponent
from components.intent_components import WantsToUseComponent, WantsToDropComponent, WantsToRemoveItemComponent
from components.character_components import AutopickupComponent
from components.name_components import NameComponent
from components.ranged_component import RangedComponent
from components.targeting_component import TargetingComponent
from components.equip_components import EquippedComponent
from state import States
from texts import Texts
import config


def get_available_item_actions(item):
    item_weapon = World.get_entity_component(item, MeleeWeaponComponent)
    item_equipped = World.get_entity_component(item, EquippedComponent)
    print(f'GET AVAILABLE ITEM ACTIONS')
    available_actions = list()
    if item_weapon:
        if item_equipped:
            # unequip
            print(f'get item actions: item equiped: Unequip')
            available_actions.append(unequip_item_from_inventory)
        else:
            # equip
            print(f'get item actions: item equiped: Equip')
            available_actions.append(select_item_from_inventory)
    else:
        # use
        available_actions.append(select_item_from_inventory)
    # drop
    available_actions.append(drop_item_from_inventory)

    return available_actions


def get_known_cursed_items_in_inventory(user):
    from components.magic_item_components import CursedItemComponent
    all_items_in_inventory = get_items_in_inventory(user)
    master_dungeon = World.fetch('master_dungeon')
    known_cursed_items = list()

    for item in all_items_in_inventory:
        item_named = World.get_entity_component(item, NameComponent)
        if item_named.name in master_dungeon.identified_items:
            cursed = World.get_entity_component(item, CursedItemComponent)
            if cursed:
                known_cursed_items.append(item)

    return known_cursed_items


def get_item(user):
    subjects = World.get_components(PositionComponent, ItemComponent)

    logs = World.fetch('logs')
    user_position = World.get_entity_component(user, PositionComponent)
    player = World.fetch('player')
    target_item = None

    for entity, (position, item) in subjects:
        if position.x == user_position.x and position.y == user_position.y:
            if not is_inventory_full(player):
                target_item = entity
            else:
                if user == player:
                    logs.appendleft(f'[color={config.COLOR_SYS_MSG}]{Texts.get_text("INVENTORY_FULL")}[/color]')

    if user == player:
        if not target_item:
            if not World.get_entity_component(player, AutopickupComponent): # dont flood player in autopickup
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]{Texts.get_text("NOTHING_TO_PICK_UP")}[/color]')
        else:
            pickup = WantsToPickUpComponent(user, target_item)
            World.add_component(pickup, user)


def is_inventory_full(user):
    items_in_backpack = get_items_in_inventory(user)
    print(f'items in backpack : {len(items_in_backpack)}')
    if len(items_in_backpack) > 25:
        return True
    return False


def use_item(item_id, target_position=None):
    player = World.fetch('player')
    use_intent = WantsToUseComponent(item_id, target_position)
    World.add_component(use_intent, player)


def drop_item_from_inventory(item_id):
    drop_intent = WantsToDropComponent(item_id)
    player = World.fetch('player')
    World.add_component(drop_intent, player)
    return States.TICKING


def unequip_item_from_inventory(item_id):
    print(f'unequip item : {item_id}')
    player = World.fetch('player')
    unequip_intent = WantsToRemoveItemComponent(item_id)
    World.add_component(unequip_intent, player)
    return States.TICKING


def select_item_from_inventory(item_id):
    print(f'select item : item id {item_id}')
    player = World.fetch('player')
    ranged = World.get_entity_component(item_id, RangedComponent)
    if ranged:
        target_intent = TargetingComponent(item_id, ranged.range)
        World.add_component(target_intent, player)
        logs = World.fetch('logs')
        logs.appendleft(f'[color={config.COLOR_SYS_MSG}]{Texts.get_text("SELECT_TARGET")} '
                        f'{Texts.get_text("ESCAPE_TO_CANCEL")}[/color]')
        return States.SHOW_TARGETING
    use_item(item_id)
    return States.TICKING


def get_items_in_user_backpack(user):
    subjects = World.get_components(NameComponent, InBackPackComponent)

    items_in_user_backpack = list()
    for entity, (name, in_backpack, *args) in subjects:
        if in_backpack.owner == user:
            items_in_user_backpack.append(entity)
    return items_in_user_backpack


def get_equipped_items(user):
    subjects = World.get_components(NameComponent, EquippedComponent)
    items_equipped_by_user = list()
    for entity, (name, equipped, *args) in subjects:
        if equipped.owner == user:
            items_equipped_by_user.append(entity)

    return items_equipped_by_user


def get_items_in_inventory(user):
    items_in_inventory = get_equipped_items(user)
    items_in_inventory.extend(get_items_in_user_backpack(user))
    return items_in_inventory
