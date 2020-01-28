from random import randint

from systems.system import System
from world import World
from effects.effects_system import add_effect, EffectType, Targets, Effect, TargetType
from components.intent_components import WantsToMeleeComponent
from components.name_components import NameComponent
from components.pools_component import Pools
from components.character_components import AttributesComponent
from components.item_components import MeleeWeaponComponent, WearableComponent
from components.equip_components import EquippedComponent
from components.skills_component import SkillsComponent, Skills
from components.natural_attack_defense_component import NaturalAttackDefenseComponent
from components.position_components import PositionComponent
from player_systems.game_system import skill_level
from player_systems.initiative_costs_mecanisms import calculate_fight_cost
from texts import Texts
from data.components_enum import EquipmentSlots, WeaponAttributes
import config


class MeleeCombatSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToMeleeComponent, NameComponent, Pools, AttributesComponent)
        if not subjects:
            return

        for entity, (wants_melee, attacker_name, attacker_pools, attacker_attributes) in subjects:
            target_pools = World.get_entity_component(wants_melee.target, Pools)
            # Attacker & defender Not dead
            if attacker_pools.hit_points.current > 0 and target_pools.hit_points.current > 0:
                # Logs
                target_name = World.get_entity_component(wants_melee.target, NameComponent).name
                logs = World.fetch('logs')

                # HIT ROLL
                natural_roll = randint(1, 20)
                if natural_roll == 1:
                    logs.appendleft(f'{Texts.get_text("FAIL_TO_HIT").format(Texts.get_text(attacker_name.name), Texts.get_text(target_name))}')
                    add_effect(None, Effect(EffectType.PARTICULE,
                                            glyph='*',
                                            fg=config.COLOR_PARTICULE_MISS,
                                            sprite='particules/miss.png',
                                            lifetime=1),
                               Targets(TargetType.SINGLE, target=wants_melee.target))
                    continue

                # Opponents infos
                attacker_skill = World.get_entity_component(entity, SkillsComponent)
                attacker_natural_attacks = World.get_entity_component(entity, NaturalAttackDefenseComponent)

                # attacker has weapon?
                weapon_entity = None
                weapon_info = get_virtual_bare_hands_weapon(entity)

                wielded_weapons = World.get_components(EquippedComponent, MeleeWeaponComponent)
                for wielden_weapon, (wielded, melee) in wielded_weapons:
                    if wielded.owner == entity and wielded.slot == EquipmentSlots.MELEE:
                        weapon_info = melee
                        weapon_entity = wielden_weapon
                # natural attack?
                if attacker_natural_attacks:
                    if randint(0, 100) <= config.DEFAULT_NATURAL_ATTACK_CHOICE:
                        rand = randint(0, len(attacker_natural_attacks.attacks) - 1)
                        weapon_info = attacker_natural_attacks.attacks[rand]

                target_attributes = World.get_entity_component(wants_melee.target, AttributesComponent)
                target_skills = World.get_entity_component(wants_melee.target, SkillsComponent)

                # To hit calculation
                attacker_attribute_hit_bonus = 0
                if weapon_info:
                    if weapon_info.attribute == WeaponAttributes.MIGHT:
                        attacker_attribute_hit_bonus += attacker_attributes.might.bonus_value
                    elif weapon_info.attribute == WeaponAttributes.QUICKNESS:
                        attacker_attribute_hit_bonus += attacker_attributes.quickness.bonus_value

                attacker_skill_melee = skill_level(attacker_skill, Skills.MELEE)
                attacker_weapon_hit_bonus = 0
                modified_hit_roll = natural_roll + attacker_attribute_hit_bonus + \
                                    attacker_skill_melee + attacker_weapon_hit_bonus

                # Defense calculation
                dodge_quickness_bonus = target_attributes.quickness.bonus_value
                dodge_skill_dodge = skill_level(target_skills, Skills.DODGE)
                dodge_item_bonus = 0
                dodge_difficulty = dodge_quickness_bonus + dodge_skill_dodge + dodge_item_bonus

                # To Hit resolution
                if not natural_roll == 20 and not modified_hit_roll > dodge_difficulty:
                    # fail
                    logs.appendleft(f'{Texts.get_text("MISS_HIT").format(Texts.get_text(attacker_name.name), Texts.get_text(target_name))}')
                    add_effect(None, Effect(EffectType.PARTICULE,
                                            glyph='*',
                                            fg=config.COLOR_PARTICULE_MISS,
                                            sprite='particules/miss.png',
                                            lifetime=1),
                               Targets(TargetType.SINGLE, target=wants_melee.target))
                    continue

                # success Hit
                # Damage calculation
                if weapon_info:
                    base_dmg = randint(weapon_info.min_dmg, weapon_info.max_dmg)
                    base_dmg += weapon_info.dmg_bonus
                else:
                    base_dmg = randint(config.DEFAULT_MIN_DMG, config.DEFAULT_MAX_DMG)
                attack_dmg = max(0, base_dmg + attacker_attributes.might.bonus_value + attacker_skill_melee)

                # armor mitigation calculation
                target_armor = target_attributes.body.bonus_value
                natural_target_armor = World.get_entity_component(wants_melee.target, NaturalAttackDefenseComponent)
                if natural_target_armor:
                    target_armor += natural_target_armor.natural_armor
                wearable_armors = World.get_components(EquippedComponent, WearableComponent)
                for wearable_armor, (equipped, wearable) in wearable_armors:
                    if equipped.owner == wants_melee.target:
                        target_armor += wearable.armor
                armor_roll = randint(0, target_armor)
                attack_dmg = max(0, attack_dmg - armor_roll)

                if attack_dmg:
                    add_effect(entity, Effect(EffectType.DAMAGE, damage=attack_dmg), Targets(TargetType.SINGLE, target=wants_melee.target))
                else:
                    logs.appendleft(
                        f'{Texts.get_text("UNABLE_TO_HURT").format(Texts.get_text(attacker_name.name), Texts.get_text(target_name))}')
                    add_effect(None, Effect(EffectType.PARTICULE,
                                            glyph='*',
                                            fg=config.COLOR_PARTICULE_NO_HURT,
                                            sprite='particules/miss.png',
                                            lifetime=1),
                               Targets(TargetType.SINGLE, target=wants_melee.target))

                # initiative cost
                World.add_component(calculate_fight_cost(entity), entity)

                # proc chance: Hit is enough, no check on damage or not
                if weapon_info.proc_chance:
                    if randint(1, 100) <= weapon_info.proc_chance:
                        if weapon_info.proc_target == 'self':
                            target = 0
                        else:
                            target = wants_melee.target
                        add_effect(entity,
                                   Effect(EffectType.ITEM_USE, item=weapon_entity),
                                   Targets(TargetType.SINGLE, target=target))

        World.remove_component_for_all_entities(WantsToMeleeComponent)


def get_virtual_bare_hands_weapon(entity):
    virtual_bare_hands = MeleeWeaponComponent(attribute=WeaponAttributes.MIGHT,
                                              min_dmg=config.DEFAULT_MIN_DMG,
                                              max_dmg=config.DEFAULT_MAX_DMG,
                                              hit_bonus=0,
                                              dmg_bonus=0,
                                              proc_chance=None,
                                              proc_target=None
                                              )
    return virtual_bare_hands