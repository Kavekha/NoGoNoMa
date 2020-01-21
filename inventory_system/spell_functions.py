from world import World

from components.pools_component import Pools
from components.spell_components import KnownSpells
from components.ranged_component import RangedComponent
from components.intent_components import WantsToCastSpellComponent
from components.targeting_component import TargetingComponent

from data_raw_master.load_raws import find_spell_entity
from texts import Texts
import config
from state import States


def cast_spell(entity_id, target_position):
    player = World.fetch('player')
    use_intent = WantsToCastSpellComponent(entity_id, target_position)
    World.add_component(use_intent, player)


def get_known_spells(user):
    known_spells_comp = World.get_entity_component(user, KnownSpells)
    known_spells = list()
    for spell in known_spells_comp.spells:
        known_spells.append(spell.display_name)

    return known_spells


def try_to_cast_spell(caster, known_spell_to_cast):
    # known_spell_to_cast: index in known spells.spells list
    pools = World.get_entity_component(caster, Pools)
    known_spells = World.get_entity_component(caster, KnownSpells)
    if pools and known_spells:
        if pools.mana_points.current >= known_spells.spells[known_spell_to_cast].mana_cost:
            spell_entity = find_spell_entity(known_spells.spells[0].display_name)
            ranged = World.get_entity_component(spell_entity, RangedComponent)
            if ranged:
                target_intent = TargetingComponent(spell_entity, ranged.range)
                World.add_component(target_intent, caster)
                logs = World.fetch('logs')
                logs.appendleft(f'[color={config.COLOR_SYS_MSG}]{Texts.get_text("SELECT_TARGET")} '
                                f'{Texts.get_text("ESCAPE_TO_CANCEL")}[/color]')
                print(f'spell has range')
                return States.SHOW_TARGETING
            World.add_component(WantsToCastSpellComponent(spell_id=spell_entity),
                                caster)
            return States.TICKING
        else:
            logs = World.fetch('logs')
            logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_NOT}]{Texts.get_text("NOT_ENOUGH_MANA")}[/color]')
    return States.TICKING
