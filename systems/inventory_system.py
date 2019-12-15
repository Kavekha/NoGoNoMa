from systems.system import System
from world import World

from components.wants_to_pickup_component import WantsToPickUpComponent
from components.position_component import PositionComponent
from components.items_component import ItemComponent
from components.wants_use_item_component import WantsToUseComponent
from components.wants_to_drop_component import WantsToDropComponent
from components.name_component import NameComponent
from components.in_backpack_component import InBackPackComponent
from components.ranged_component import RangedComponent
from components.targeting_component import TargetingComponent
from state import States
from texts import Texts
import config


class ItemCollectionSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToPickUpComponent)
        if not subjects:
            return

        player = World.fetch('player')
        logs = World.fetch('logs')
        for entity, (wants_to_pick, *args) in subjects:
            # Remove item position component.
            World.remove_component(PositionComponent, wants_to_pick.item)
            backpack = InBackPackComponent(entity)
            World.add_component(backpack, wants_to_pick.item)

            if wants_to_pick.collected_by == player:
                item_name = World.get_entity_component(wants_to_pick.item, NameComponent)
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_OK}]{Texts.get_text("YOU_PICK_UP")}'
                                f'{Texts.get_text(item_name.name)}[/color]')

            World.remove_component(WantsToPickUpComponent, entity)


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
                item_name = World.get_entity_component(wants_to_drop.item, NameComponent)
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]{Texts.get_text("YOU_DROP_UP")}'
                                f'{item_name.name}[/color]')

            World.remove_component(WantsToDropComponent, entity)


def get_item(user):
    subjects = World.get_components(PositionComponent, ItemComponent)
    if not subjects:
        return

    logs = World.fetch('logs')
    user_position = World.get_entity_component(user, PositionComponent)
    player = World.fetch('player')
    target_item = ''

    for entity, (position, item) in subjects:
        if position.x == user_position.x and position.y == user_position.y:
            target_item = entity

    if user == player:
        if not target_item:
            logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]{Texts.get_text("NOTHING_TO_PICK_UP")}[/color]')
        else:
            pickup = WantsToPickUpComponent(user, target_item)
            World.add_component(pickup, user)


def use_item(item_id, target_position=None):
    player = World.fetch('player')
    use_intent = WantsToUseComponent(item_id, target_position)
    World.add_component(use_intent, player)


def drop_item_from_inventory(item_id):
    drop_intent = WantsToDropComponent(item_id)
    player = World.fetch('player')
    World.add_component(drop_intent, player)


def select_item_from_inventory(item_id):
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
    return States.PLAYER_TURN


def get_items_in_user_backpack(user):
    subjects = World.get_components(NameComponent, InBackPackComponent)

    items_in_user_backpack = []
    for entity, (name, in_backpack, *args) in subjects:
        if in_backpack.owner == user:
            items_in_user_backpack.append(entity)

    return items_in_user_backpack
