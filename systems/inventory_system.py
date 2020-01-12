from systems.system import System
from world import World

from components.intent_components import WantsToPickUpComponent
from components.position_components import PositionComponent
from components.item_components import ItemComponent, InBackPackComponent
from components.intent_components import WantsToUseComponent, WantsToDropComponent
from components.character_components import AutopickupComponent
from components.name_components import NameComponent
from components.ranged_component import RangedComponent
from components.targeting_component import TargetingComponent
from components.equip_components import EquippedComponent
from state import States
from texts import Texts
from ui_system.render_functions import get_obfuscate_name
import config


class ItemDropSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToDropComponent)
        if not subjects:
            return

        player = World.fetch('player')
        logs = World.fetch('logs')
        for entity, (wants_to_drop, *args) in subjects:
            entity_position = World.get_entity_component(entity, PositionComponent)
            drop_position = PositionComponent(entity_position.x, entity_position.y)
            World.add_component(drop_position, wants_to_drop.item)
            World.remove_component(InBackPackComponent, wants_to_drop.item)

            if entity == player:
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]{Texts.get_text("YOU_DROP_UP")}'
                                f'{get_obfuscate_name(wants_to_drop.item)}[/color]')

            World.remove_component(WantsToDropComponent, entity)


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
    print(f'use item: player has wants to use? : {World.get_entity_component(player, WantsToUseComponent)}')


def drop_item_from_inventory(item_id):
    drop_intent = WantsToDropComponent(item_id)
    player = World.fetch('player')
    World.add_component(drop_intent, player)
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
