from collections import deque
from random import seed

from world import World
from effects.effects_system import EffectSystem
from systems.visibility_system import VisibilitySystem
from systems.monster_ai_system import MonsterAi
from systems.map_indexing_system import MapIndexingSystem
from systems.melee_combat_system import MeleeCombatSystem
from systems.damage_system import DamageSystem
from systems.particule_system import ParticuleSpawnSystem

from inventory_system.item_collection_system import ItemCollectionSystem
from inventory_system.use_equip_system import UseEquipSystem
from inventory_system.item_use_system import ItemUseSystem

from systems.inventory_system import ItemDropSystem
from systems.item_identification_system import ItemIdentificationSystem
from systems.trigger_system import TriggerSystem
from systems.initiative_system import InitiativeSystem
from gmap.master_dungeon import MasterDungeon
from gmap.spawner import spawn_player

from texts import Texts


def init_game(master_seed=None):
    if master_seed:
        seed(master_seed)
        World.insert('seed', master_seed)

    # create systems.
    item_collection_system = ItemCollectionSystem()
    World.add_system(item_collection_system)

    use_equip_system = UseEquipSystem()
    World.add_system(use_equip_system)

    item_use_system = ItemUseSystem()
    World.add_system(item_use_system)

    drop_system = ItemDropSystem()
    World.add_system(drop_system)

    identification_system = ItemIdentificationSystem()
    World.add_system(identification_system)

    visibility_system = VisibilitySystem()
    World.add_system(visibility_system)

    map_indexing_system = MapIndexingSystem()
    World.add_system(map_indexing_system)

    trigger_system = TriggerSystem()
    World.add_system(trigger_system)

    monster_ai_system = MonsterAi()
    World.add_system(monster_ai_system)

    melee_combat_system = MeleeCombatSystem()
    World.add_system(melee_combat_system)
    damage_system = DamageSystem()
    World.add_system(damage_system)

    effect_system = EffectSystem()
    World.add_system(effect_system)

    particule_spawn_system = ParticuleSpawnSystem()
    World.add_system(particule_spawn_system)

    initiative_system = InitiativeSystem()
    World.add_system(initiative_system)

    # add player position to ressources
    player = spawn_player(0, 0)
    World.insert('player', player)

    master_dungeon = MasterDungeon()
    World.insert('master_dungeon', master_dungeon)
    state = World.fetch('state')
    state.generate_world_map(1)

    # add logs
    log_entry = deque()
    log_entry.append(Texts.get_text("WELCOME_MESSAGE"))
    World.insert('logs', log_entry)

    # add tooltips
    tooltip = list()
    World.insert('tooltip', (tooltip, 0, 0))
