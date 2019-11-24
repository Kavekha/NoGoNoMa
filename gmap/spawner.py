from random import randint

from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent
from components.viewshed_component import ViewshedComponent
from components.name_component import NameComponent
from components.monster_component import MonsterComponent
from components.blocktile_component import BlockTileComponent
from components.combat_stats_component import CombatStatsComponent
from components.player_component import PlayerComponent

from data.types import Layers
from data.items_creation import create_healing_potion_item, create_magic_missile_scroll, create_fireball_scroll, \
    create_confusion_scroll
from world import World
import config


def spawn_world(current_map):
    for room in current_map.rooms:
        if len(current_map.rooms) > 0 and room != current_map.rooms[0]:
            spawn_room(room)


def spawn_room(room):
    nb_mobs = randint(1, config.MAX_MONSTERS_ROOM +2) -3
    nb_items = randint(1, config.MAX_ITEMS_ROOM +2) -3

    current_map = World.fetch('current_map')

    monster_position_to_spawn = random_room_positions_list(nb_mobs, current_map, room)
    for idx in monster_position_to_spawn:
        x, y = current_map.index_to_point2d(idx)
        create_random_monster(x, y)

    item_position_to_spawn = random_room_positions_list(nb_items, current_map, room)
    for idx in item_position_to_spawn:
        x, y = current_map.index_to_point2d(idx)
        create_random_item(x, y)


def random_room_positions_list(nb_iterations, current_map, room):
    position_list = []

    for _i in range(0, nb_iterations):
        added = False
        while not added:
            x = room.x1 + randint(1, abs(room.x2 - room.x1))
            y = room.y1 + randint(1, abs(room.y2 - room.y1))
            idx = current_map.xy_idx(x, y)
            if idx not in position_list:
                position_list.append(idx)
                added = True
    return position_list


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


def create_monster(name, x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent('g', 'red', Layers.MONSTER)
    name = NameComponent(name)
    viewshed = ViewshedComponent(8)
    block = BlockTileComponent()
    monster_component = MonsterComponent()
    combat_stats = CombatStatsComponent(16, 1, 4)
    monster_id = World.create_entity(position, renderable, viewshed, name, monster_component, block, combat_stats)
    return monster_id


def create_random_monster(x, y):
    monster_list = ['Orc', 'Morblin']
    name = monster_list[randint(0, len(monster_list) -1)]

    return create_monster(name, x, y)


def create_random_item(x, y):
    rand = randint(0, 3)
    if rand == 1:
        return create_healing_potion_item(x, y)
    elif rand == 2:
        return create_magic_missile_scroll(x, y)
    elif rand == 3:
        return create_confusion_scroll(x, y)
    else:
        return create_fireball_scroll(x, y)



