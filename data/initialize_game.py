from collections import deque
from random import seed

from world import World
import config
from systems.visibility_system import VisibilitySystem
from systems.monster_ai_system import MonsterAi
from systems.map_indexing_system import MapIndexingSystem
from systems.melee_combat_system import MeleeCombatSystem
from systems.damage_system import DamageSystem
from ui_system.ui_system import UiSystem
from systems.inventory_system import ItemCollectionSystem, ItemDropSystem
from systems.item_use_system import ItemUseSystem
from gmap.map_creation import Gmap
from gmap.spawner import spawn_world, spawn_player
from texts import Texts


def init_game(master_seed=None):
    if master_seed:
        seed(master_seed)
        World.insert('seed', master_seed)

    # create systems.
    visibility_system = VisibilitySystem()
    World.add_system(visibility_system)
    monster_ai_system = MonsterAi()
    World.add_system(monster_ai_system)
    map_indexing_system = MapIndexingSystem()
    World.add_system(map_indexing_system)
    melee_combat_system = MeleeCombatSystem()
    World.add_system(melee_combat_system)
    damage_system = DamageSystem()
    World.add_system(damage_system)
    ui_system = UiSystem()
    World.add_system(ui_system)
    inventory_system = ItemCollectionSystem()
    World.add_system(inventory_system)
    drop_system = ItemDropSystem()
    World.add_system(drop_system)
    item_use_system = ItemUseSystem()
    World.add_system(item_use_system)

    # create map
    current_map = Gmap(1)
    World.insert('current_map', current_map)

    # create entities in current_map
    spawn_world(current_map)

    # add player position to ressources
    x, y = current_map.rooms[0].center()
    player = spawn_player(x, y)
    World.insert('player', player)

    # add logs
    log_entry = deque()
    log_entry.append(Texts.get_text("WELCOME_MESSAGE"))
    World.insert('logs', log_entry)
