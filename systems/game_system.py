import config


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
    if skill in skill_component.skills:
        return skill_component.skills[skill]
    return config.DEFAULT_NO_SKILL_VALUE
