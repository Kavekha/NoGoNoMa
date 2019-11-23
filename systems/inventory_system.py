from systems.system import System
from world import World

from components.wants_to_pickup_component import WantsToPickUpComponent
from components.name_component import NameComponent
from components.in_backpack_component import InBackPackComponent
from components.position_component import PositionComponent
from components.item_component import ItemComponent
from components.wants_to_drop_component import WantsToDropComponent
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
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_OK}]You pick up: {item_name.name}[/color]')

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
                logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]You drop up : {item_name.name}[/color]')

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
            logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]There is nothing here to pick up.[/color]')
        else:
            pickup = WantsToPickUpComponent(user, target_item)
            World.add_component(pickup, user)




