from random import randint

from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent
from components.viewshed_component import ViewshedComponent
from components.name_component import NameComponent
from components.blocktile_component import BlockTileComponent
from components.combat_stats_component import CombatStatsComponent
from components.player_component import PlayerComponent

from ui_system.ui_enums import Layers
from data.random_table import room_table
from data.items_creation import create_healing_potion_item, create_magic_missile_scroll, create_fireball_scroll, \
    create_confusion_scroll, create_dagger, create_shield, create_long_sword, create_tower_shield
from data.monsters_creation import create_monster_morblin, create_monster_orcish
from world import World
from gmap.utils import xy_idx, index_to_point2d
from data.load_raws import RawsMaster
import config


def spawn_world(current_map):
    for room in current_map.rooms:
        if len(current_map.rooms) > 0 and room != current_map.rooms[0]:
            spawn_room(room)


def monster_and_items_list():
    monster_list = {
        'morblin': create_monster_morblin,
        'orcish': create_monster_orcish,
        "health potion": create_healing_potion_item,
        'missile Magic Scroll': create_magic_missile_scroll,
        "fireball scroll": create_fireball_scroll,
        'confusion scroll': create_confusion_scroll,
        'dagger': create_dagger,
        'shield': create_shield,
        'longsword': create_long_sword,
        'tower shield': create_tower_shield
    }
    return monster_list


def spawn_room(room):
    current_map = World.fetch('current_map')
    current_depth = current_map.depth
    spawn_table = room_table(current_depth)
    spawn_points = []
    num_spawns = randint(1, config.MAX_MONSTERS_ROOM + 3) + (current_depth - 1) - 3
    # monster_list = monster_and_items_list()

    for _i in range(0, num_spawns):
        added = False
        tries = 0
        while not added and tries < 20:
            x = room.x1 + randint(1, abs(room.x2 - room.x1) -2)
            y = room.y1 + randint(1, abs(room.y2 - room.y1) -2)
            idx = xy_idx(x, y)
            if idx not in spawn_points:
                spawn_points.append((idx, spawn_table.roll()))
                added = True
            else:
                tries += 1

    for idx, spawn in spawn_points:
        x, y = index_to_point2d(idx)
        try:
            print(f'idx spawn in spawn points is {spawn}')
            RawsMaster.spawn_named_entity(spawn, x, y)
            print(f'{World.get_all_entities()}')
        except:
            print(f'Spawner:spawn room: {spawn} requested, but doesnt appear in monster list')


def spawn_player(x, y):
    # Entity Name, Pos & Rend & PLAYER
    x, y = x, y
    pos = PositionComponent(x, y)
    rend = RenderableComponent('@', 'yellow', Layers.PLAYER)
    name = NameComponent('Player')
    viewshed = ViewshedComponent()
    player = PlayerComponent()
    block = BlockTileComponent()
    combat_stats = CombatStatsComponent(30, 2, 5)
    player_id = World.create_entity(pos, rend, name, player, viewshed, block, combat_stats)
    return player_id
