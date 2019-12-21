from random import randint

from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent
from components.viewshed_component import ViewshedComponent
from components.name_component import NameComponent
from components.blocktile_component import BlockTileComponent
from components.player_component import PlayerComponent
from components.attributes_component import AttributesComponent
from components.skills_component import SkillsComponent, Skills
from components.pools_component import Pools

from ui_system.ui_enums import Layers
from player_systems.game_system import player_hp_at_level, mana_point_at_level
from world import World
from gmap.gmap_enums import TileType
from data.load_raws import RawsMaster
import config


def spawn_world(current_map):
    current_map.spawn_table = RawsMaster.get_spawn_table_for_depth(current_map.depth)
    for room in current_map.rooms:
        if len(current_map.rooms) > 0 and room != current_map.rooms[0]:
            spawn_room(room, current_map)


def spawn_entity(spawn_name, spawn_point, current_map):
    x = int(spawn_point % current_map.width)
    y = spawn_point // current_map.width
    try:
        print(f'idx spawn in spawn points is {spawn_name}')
        RawsMaster.spawn_named_entity(spawn_name, x, y)
        # print(f'{World.get_all_entities()}')
    except:
        print(f'Spawner:spawn room: {spawn_name} requested, not generated because error.')


def spawn_room(room, current_map):
    possible_targets = []
    for y in range(room.y1, room.y2 + 1):
        for x in range(room.x1, room.x2 + 1):
            idx = current_map.xy_idx(x, y)
            if current_map.tiles[idx] == TileType.FLOOR:
                possible_targets.append(idx)

    spawn_region(possible_targets, current_map)


def spawn_region(list_of_spawn_idx, current_map):
    num_spawns = min(len(list_of_spawn_idx) - 1, randint(1, config.MAX_MONSTERS_ROOM + 3) + current_map.depth - 1)
    current_map.spawn_table = RawsMaster.get_spawn_table_for_depth(current_map.depth)
    if not num_spawns:
        return
    spawn_points = list()

    for i in range(0, num_spawns):
        spawn_points.append((list_of_spawn_idx[i], current_map.spawn_table.roll()))

    for idx, spawn in spawn_points:
        spawn_entity(spawn, idx, current_map)


def spawn_player(x, y):
    # Entity Name, Pos & Rend & PLAYER
    x, y = x, y
    pos = PositionComponent(x, y)
    rend = RenderableComponent(glyph='@',
                               char_color='white',
                               render_order=Layers.PLAYER,
                               sprite='chars/player.png')
    name = NameComponent('Player')
    viewshed = ViewshedComponent()
    player = PlayerComponent()
    block = BlockTileComponent()
    attributes = AttributesComponent(might=config.DEFAULT_PLAYER_MIGHT_ATTRIBUTE,
                                     body=config.DEFAULT_PLAYER_BODY_ATTRIBUTE,
                                     quickness=config.DEFAULT_PLAYER_QUICKNESS_ATTRIBUTE,
                                     wits=config.DEFAULT_PLAYER_WITS_ATTRIBUTE)
    skills = SkillsComponent()
    skills.skills[Skills.MELEE] = 1
    skills.skills[Skills.DODGE] = 1
    player_pool = Pools(hits=player_hp_at_level(attributes.body, 1), mana=mana_point_at_level(attributes.wits, 1))
    player_id = World.create_entity(pos, rend, name, player, viewshed, block, attributes, skills, player_pool)
    return player_id
