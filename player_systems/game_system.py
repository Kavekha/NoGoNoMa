import config
from world import World
from texts import Texts
from components.pools_component import Pools
from components.attributes_component import AttributesComponent


def player_gain_xp(xp_gain):
    if xp_gain:
        player = World.fetch('player')
        player_pool = World.get_entity_component(player, Pools)
        player_attributes = World.get_entity_component(player, AttributesComponent)
        logs = World.fetch('logs')

        player_pool.xp += xp_gain
        while player_pool.xp >= xp_for_next_level(player_pool.level):
            player_pool.level += 1
            player_pool.hit_points.max = player_hp_at_level(player_attributes.body, player_pool.level)
            player_pool.hit_points.current += min(player_pool.hit_points.max, player_hp_per_level(player_attributes.body))
            player_pool.mana_points.max = mana_point_at_level(player_attributes.wits, player_pool.level)
            player_pool.mana_points.current = min(player_pool.mana_points.max, mana_per_level(player_attributes.wits))
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
    return config.DEFAULT_HIT_POINTS + body


def player_hp_at_level(body, lvl):
    return player_hp_per_level(body) * lvl


def npc_hp_at_lvl(body, lvl):
    total = 1
    for _i in range(0, lvl):
        total += max(1, config.DEFAULT_MONSTER_HIT_POINTS + body)
    return total


def mana_per_level(wits):
    return max(1, config.DEFAULT_MANA_POINTS + wits)


def mana_point_at_level(wits, lvl):
    return mana_per_level(wits) * lvl


def skill_level(skill_component, skill):
    print(f'skill level for {skill}, in skills {skill_component.skills}')
    if skill in skill_component.skills:
        return skill_component.skills[skill]
    return config.DEFAULT_NO_SKILL_VALUE
