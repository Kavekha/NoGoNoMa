from enum import Enum

from components.in_backpack_component import InBackPackComponent
from components.equipped_component import EquippedComponent
from player_systems.game_system import player_gain_xp, xp_for_next_depth
from world import World
import config
from texts import Texts
from gmap.utils import level_transition


class States(Enum):
    AWAITING_INPUT = 0
    PRE_RUN = 1
    PLAYER_TURN = 2
    MONSTER_TURN = 3
    SHOW_INVENTORY = 4
    SHOW_SELECTED_ITEM_MENU = 5
    SHOW_TARGETING = 6
    MAIN_MENU = 7
    LOAD_GAME = 8
    SAVE_GAME = 9
    NEXT_LEVEL = 10
    GAME_OVER = 11
    VICTORY = 12
    CHARACTER_SHEET = 13
    OPTION_MENU = 14
    MAP_GENERATION = 15


class State:
    def __init__(self, state):
        self.current_state = state
        self.mapgen_index = 0
        self.mapgen_history = list()
        self.mapgen_timer = 0
        self.args = None

    def change_state(self, new_state):
        # if new_state != self.current_state:
            # print(f'new state required for {self}: from {self.current_state} to {new_state}')
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
        self.generate_world_map(current_map.depth + 1)

        current_map = World.fetch('current_map')
        logs = World.fetch('logs')
        logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]{Texts.get_text("GO_NEXT_LEVEL")}[/color]')
        player_gain_xp(xp_for_next_depth(current_map.depth - 1))

    def generate_world_map(self, new_depth):
        self.mapgen_index = 0
        self.mapgen_timer = 0
        self.mapgen_history.clear()

        self.mapgen_history = level_transition(new_depth)
        print(f'generate world : map gen history is : {self.mapgen_history}')
