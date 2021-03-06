from random import randint

import config
from world import World
from texts import Texts
from ui_system.render_functions import get_obfuscate_name
from components.pools_component import Pools
from components.character_components import AttributesComponent
from components.skills_component import SkillsComponent
from components.blocktile_component import BlockVisibilityComponent, BlockTileComponent
from components.renderable_component import RenderableComponent
from components.magic_item_components import CursedItemComponent, MagicItemComponent
from components.name_components import NameComponent, ObfuscatedNameComponent
from components.item_components import ItemComponent


def item_identified(item):
    # doublon de item identification system.
    item_named = World.get_entity_component(item, NameComponent)
    master_dungeon = World.fetch('master_dungeon')
    master_dungeon.identified_items.add(item_named.name)

    for entity_item, (_item, named) in World.get_components(ItemComponent, NameComponent):
        if named.name == item_named.name:
            World.remove_component(ObfuscatedNameComponent, entity_item)

    logs = World.fetch('logs')
    logs.appendleft(f'[color={config.COLOR_SYS_MSG}]'
                    f'{Texts.get_text("YOU_IDENTIFIED_")}'
                    f'{Texts.get_text(item_named.name)}.')


def remove_curse_on_item(item):
    World.remove_component(CursedItemComponent, item)
    magic_item = World.get_entity_component(item, MagicItemComponent)
    if magic_item:
        magic_item.cursed = False
    logs = World.fetch('logs')
    logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_OK}]{Texts.get_text("CURSE_REMOVED_ON_")}'
                    f'{get_obfuscate_name(item)}[/color]')


def opening_door(door_id, door_component):
    print(f'opening door {door_id}')
    door_component.close = False
    World.remove_component(BlockVisibilityComponent, door_id)
    World.remove_component(BlockTileComponent, door_id)
    renderable = World.get_entity_component(door_id, RenderableComponent)
    renderable.glyph = '/'
    renderable.sprite = 'props/door_open.png'


def player_gain_xp(xp_gain):
    if xp_gain:
        player = World.fetch('player')
        player_pool = World.get_entity_component(player, Pools)
        player_attributes = World.get_entity_component(player, AttributesComponent)
        logs = World.fetch('logs')

        player_pool.xp += xp_gain
        while player_pool.xp >= xp_for_next_level(player_pool.level):
            player_pool.level += 1
            player_pool.hit_points.max = player_hp_at_level(player_attributes.body,
                                                            player_pool.level)
            player_pool.hit_points.current += min(player_pool.hit_points.max,
                                                  player_hp_per_level(player_attributes.body))
            player_pool.mana_points.max = mana_point_at_level(player_attributes.wits,
                                                              player_pool.level)
            player_pool.mana_points.current = min(player_pool.mana_points.max,
                                                  mana_per_level(player_attributes.wits))
            logs.appendleft(f'[color={config.COLOR_SYS_MSG}]'
                                    f'{Texts.get_text("YOU_ARE_NOW_LEVEL").format(player_pool.level)}[/color]')


def calculate_xp_from_entity(entity_id):
    entity_pools = World.get_entity_component(entity_id, Pools)
    xp_gain = config.XP_GAIN_PER_MONSTER_LVL * entity_pools.level * config.XP_GAIN_MULTIPLIER * entity_pools.level
    return xp_gain


def xp_for_next_level(current_level):
    xp_needed = current_level * config.XP_PER_LEVEL * (current_level * config.XP_MULTIPLIER)
    return xp_needed


def xp_for_next_depth(depth_cleared):
    return depth_cleared * config.XP_PER_DEPTH * config.XP_DEPTH_MULTIPLIER


def player_hp_per_level(body):
    return config.DEFAULT_HIT_POINTS + body.bonus_value


def player_hp_at_level(body, lvl):
    return player_hp_per_level(body) * lvl


def npc_hp_at_lvl(body, lvl):
    total = 1
    for _i in range(0, lvl):
        total += max(1, config.DEFAULT_MONSTER_HIT_POINTS + body.bonus_value)
    return total


def mana_per_level(wits):
    return max(1, config.DEFAULT_MANA_POINTS + wits.bonus_value)


def mana_point_at_level(wits, lvl):
    return mana_per_level(wits) * lvl


def skill_level(skill_component, skill):
    print(f'skill level for {skill}, in skills {skill_component.skills}')
    if skill in skill_component.skills:
        return skill_component.skills[skill]
    return config.DEFAULT_NO_SKILL_VALUE


def make_scroll_name():
    name = Texts.get_text('SCROLL_OF_')
    print(f'MAKE SCROLL : Name is {name}')

    length = 4 + randint(1, 4)

    for i in range(0, length):
        if i % 2 == 0:
            voyelle = ['a', 'e', 'i', 'o', 'u', 'y']
            name += voyelle[randint(0, len(voyelle) - 1)]
        else:
            consonne = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']
            name += consonne[randint(0, len(consonne) - 1)]
    return name


def make_potion_name(used_potion_names):
    while True:
        adjectives = config.POTION_ADJECTIVES
        colors = config.POTION_COLORS
        adjective = adjectives[randint(0, len(adjectives) - 1)]
        color = colors[randint(0, len(colors) - 1)]
        name = Texts.get_text('OBFUSCATE_POTION_NAME').format(Texts.get_text(adjective), Texts.get_text(color))
        if name not in used_potion_names:
            return name


def skill_roll_against_difficulty(entity, skill, difficulty):
    skills_comp = World.get_entity_component(entity, SkillsComponent)
    if skills_comp:
        skill_value = skills_comp.skills.get(skill, config.DEFAULT_NO_SKILL_VALUE)
    else:
        skill_value = config.DEFAULT_NO_SKILL_VALUE
    skill_rand = randint(0, 5 + skill_value)
    if randint(1, difficulty) <= skill_rand:
        return True
    return False

