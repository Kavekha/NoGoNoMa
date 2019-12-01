from enum import Enum

from gmap.map_creation import Gmap
from gmap.spawner import spawn_world
from components.position_component import PositionComponent
from components.viewshed_component import ViewshedComponent
from components.in_backpack_component import InBackPackComponent
from components.equipped_component import EquippedComponent
from world import World
import config


class States(Enum):
    AWAITING_INPUT = 0
    PRE_RUN = 1
    PLAYER_TURN = 2
    MONSTER_TURN = 3
    SHOW_INVENTORY = 4
    SHOW_ITEM_WINDOW = 5
    SHOW_DROP_ITEM = 6
    SHOW_TARGETING = 7
    MAIN_MENU = 8
    LOAD_GAME = 9
    SAVE_GAME = 10
    NEXT_LEVEL = 11
    GAME_OVER = 12
    VICTORY = 13


class State:
    def __init__(self, state):
        self.current_state = state

    def change_state(self, new_state):
        if new_state != self.current_state:
            print(f'new state required for {self}: from {self.current_state} to {new_state}')
        self.current_state = new_state

    def entities_to_remove_on_level_change(self):
        print('------- ENTITIES TO REMOVE ----------')
        entities = World.get_all_entities()
        to_delete = []
        player = World.fetch('player')
        print(f'entities to remove: player is now {player}')

        for entity in entities:
            should_delete = True

            if entity == player:
                should_delete = False

            backpack = World.get_entity_component(entity, InBackPackComponent)
            if backpack:
                if backpack.owner == player:
                    should_delete = False

            equipped = World.get_entity_component(entity, EquippedComponent)
            if equipped:
                if equipped.owner == player:
                    should_delete = False

            if should_delete:
                to_delete.append(entity)

        print(f'to delete: contains {to_delete}')
        return to_delete

    def go_next_level(self):
        to_delete = self.entities_to_remove_on_level_change()
        for entity in to_delete:
            World.delete_entity(entity)

        current_map = World.fetch('current_map')
        new_worldmap = Gmap(current_map.depth + 1)
        World.insert('current_map', new_worldmap)

        current_map = World.fetch('current_map')
        spawn_world(current_map)

        player = World.fetch('player')
        player_pos = World.get_entity_component(player, PositionComponent)
        player_pos.x, player_pos.y = current_map.rooms[0].center()
        player_viewshed = World.get_entity_component(player, ViewshedComponent)
        player_viewshed.dirty = True

        logs = World.fetch('logs')
        logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]You descend to the next level.[/color]')
