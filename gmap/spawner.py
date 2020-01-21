from random import randint
from itertools import product as it_product

from components.position_components import PositionComponent
from components.renderable_component import RenderableComponent
from components.viewshed_component import ViewshedComponent
from components.name_components import NameComponent
from components.blocktile_component import BlockTileComponent
from components.character_components import AttributesComponent, AutopickupComponent, PlayerComponent
from components.skills_component import SkillsComponent, Skills
from components.pools_component import Pools
from components.initiative_components import InitiativeComponent
from components.spell_components import KnownSpells, KnownSpell

from ui_system.ui_enums import Layers
from player_systems.game_system import player_hp_at_level, mana_point_at_level
from world import World
from gmap.gmap_enums import TileType
from data_raw_master.raw_master import RawsMaster
import config


def spawn_entity(spawn_name, spawn_point, current_map):
    x = int(spawn_point % current_map.width)
    y = spawn_point // current_map.width
    try:
        print(f'idx spawn in spawn points is {spawn_name}')
        RawsMaster.spawn_named_entity(spawn_name, x, y)
    except Exception as e:
        print(f'WARNING:Spawner:spawn room: {spawn_name} requested, not generated because error.')
        print(f'Error was : {e}')


def spawn_room(room, current_map, spawn_list):
    possible_targets = []
    for x, y in it_product(range(room.x1, room.x2 + 1), range(room.y1, room.y2 + 1)):
        idx = current_map.xy_idx(x, y)
        if current_map.tiles[idx] == TileType.FLOOR:
            possible_targets.append(idx)

    spawn_region(possible_targets, current_map, spawn_list)


def spawn_region(areas, current_map, spawn_list):
    current_map.spawn_table = RawsMaster.get_spawn_table_for_depth(current_map.depth)
    spawn_points = dict()

    num_spawn = min(len(areas) - 1, randint(1, config.MAX_MONSTERS_ROOM + 3)) + (current_map.depth - 1) - 3
    if not num_spawn:
        return

    for _i in range(0, num_spawn):
        if len(areas) == 1:
            areas_index = 0
        else:
            areas_index = randint(1, len(areas) - 1)
        map_idx = areas[areas_index]
        spawn_points[map_idx] = current_map.spawn_table.roll()
        areas.remove(areas[areas_index])

    for spawn in spawn_points:
        spawn_list.append((spawn, spawn_points[spawn]))  # idx, name to spawn


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
    autopickup = AutopickupComponent()
    skills = SkillsComponent()
    skills.skills[Skills.MELEE] = 1
    skills.skills[Skills.DODGE] = 1
    skills.skills[Skills.FOUND_TRAPS] = 1
    player_pool = Pools(hits=player_hp_at_level(attributes.body, 1), mana=mana_point_at_level(attributes.wits, 1))
    player_initiative = InitiativeComponent(0)

    player_id = World.create_entity(pos, rend, name, player, viewshed, block, attributes, skills, player_pool,
                                    autopickup, player_initiative)

    spell = KnownSpell('HARM', 1)
    known_spells = KnownSpells()
    known_spells.spells.append(spell)
    World.add_component(known_spells, player_id)

    return player_id
