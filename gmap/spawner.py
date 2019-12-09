from random import randint

from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent
from components.viewshed_component import ViewshedComponent
from components.name_component import NameComponent
from components.blocktile_component import BlockTileComponent
from components.combat_stats_component import CombatStatsComponent
from components.player_component import PlayerComponent
from components.attributes_component import AttributesComponent
from components.skills_component import SkillsComponent, Skills
from components.pools_component import Pools

from ui_system.ui_enums import Layers
from world import World
from gmap.utils import xy_idx, index_to_point2d
from data.load_raws import RawsMaster
import config


def spawn_world(current_map):
    current_map.spawn_table = RawsMaster.get_spawn_table_for_depth(current_map.depth)
    for room in current_map.rooms:
        if len(current_map.rooms) > 0 and room != current_map.rooms[0]:
            spawn_room(room, current_map)


def spawn_room(room, current_map):
    current_depth = current_map.depth
    spawn_points = []
    num_spawns = randint(1, config.MAX_MONSTERS_ROOM + 3) + (current_depth - 1) - 3

    for _i in range(0, num_spawns):
        added = False
        tries = 0
        while not added and tries < 20:
            x = room.x1 + randint(1, abs(room.x2 - room.x1) -2)
            y = room.y1 + randint(1, abs(room.y2 - room.y1) -2)
            idx = xy_idx(x, y)
            if idx not in spawn_points:
                spawn_points.append((idx, current_map.spawn_table.roll()))
                added = True
            else:
                tries += 1

    for idx, spawn in spawn_points:
        x, y = index_to_point2d(idx)
        try:
            print(f'idx spawn in spawn points is {spawn}')
            RawsMaster.spawn_named_entity(spawn, x, y)
            # print(f'{World.get_all_entities()}')
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
    attributes = AttributesComponent(might=config.DEFAULT_PLAYER_MIGHT_ATTRIBUTE,
                                     body=config.DEFAULT_PLAYER_BODY_ATTRIBUTE,
                                     quickness=config.DEFAULT_PLAYER_QUICKNESS_ATTRIBUTE,
                                     wits=config.DEFAULT_PLAYER_WITS_ATTRIBUTE)
    skills = SkillsComponent()
    skills.skills[Skills.MELEE] = 1
    skills.skills[Skills.DEFENSE] = 1
    player_pool = Pools(hits=30, mana=5)
    player_id = World.create_entity(pos, rend, name, player, viewshed, block, combat_stats, attributes, skills, player_pool)
    return player_id
