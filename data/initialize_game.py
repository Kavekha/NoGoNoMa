from collections import deque
from random import seed

from world import World
from effects.effects_system import EffectSystem
from systems.visibility_system import VisibilitySystem
from systems.monster_ai_system import MonsterAi
from systems.map_indexing_system import MapIndexingSystem
from systems.melee_combat_system import MeleeCombatSystem
from systems.particule_system import ParticuleSpawnSystem
from systems.item_identification_system import ItemIdentificationSystem
from systems.trigger_system import TriggerSystem
from systems.initiative_system import InitiativeSystem
from systems.turn_status_effect_system import TurnStatusEffectSystem

from inventory_system.spell_use_system import SpellUseSystem
from inventory_system.item_collection_system import ItemCollectionSystem
from inventory_system.use_equip_system import UseEquipSystem
from inventory_system.item_use_system import ItemUseSystem
from inventory_system.item_remove_system import ItemRemoveSystem
from inventory_system.drop_item_system import ItemDropSystem
from inventory_system.equipment_change_system import EquipmentChangeSystem

from gmap.master_dungeon import MasterDungeon
from gmap.spawner import spawn_player

from texts import Texts


def init_game(master_seed=None):
    if master_seed:
        seed(master_seed)
        World.insert('seed', master_seed)

    # create systems.
    World.add_system(ItemCollectionSystem())

    World.add_system(UseEquipSystem())

    World.add_system(ItemUseSystem())

    World.add_system(SpellUseSystem())

    World.add_system(ItemDropSystem())

    World.add_system(ItemRemoveSystem())

    World.add_system(ItemIdentificationSystem())

    World.add_system(EquipmentChangeSystem())

    World.add_system(VisibilitySystem())

    World.add_system(MapIndexingSystem())

    World.add_system(TriggerSystem())

    World.add_system(MonsterAi())

    World.add_system(MeleeCombatSystem())

    World.add_system(EffectSystem())

    World.add_system(ParticuleSpawnSystem())

    World.add_system(InitiativeSystem())

    World.add_system(TurnStatusEffectSystem())

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

    # spawn all spell templates.
    from data_raw_master.raw_master import RawsMaster
    RawsMaster.spawn_all_spells()
