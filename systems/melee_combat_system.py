from random import randint

from systems.system import System
from world import World
from components.wants_to_melee_component import WantsToMeleeComponent
from components.name_component import NameComponent
from components.pools_component import Pools
from components.attributes_component import AttributesComponent
from components.suffer_damage_component import SufferDamageComponent
from components.items_component import MeleeWeaponComponent, WearableComponent
from components.equipped_component import EquippedComponent
from components.skills_component import SkillsComponent, Skills
from player_systems.game_system import skill_level
from texts import Texts
from data.items_enum import EquipmentSlots, WeaponAttributes
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
                    logs.appendleft(f'{Texts.get_text("FAIL_TO_HIT").format(attacker_name.name, target_name)}')
                    World.remove_component(WantsToMeleeComponent, entity)
                    continue

                # Opponents infos
                attacker_skill = World.get_entity_component(entity, SkillsComponent)
                # attacker has weapon?
                weapon_info = None
                wielded_weapons = World.get_components(EquippedComponent, MeleeWeaponComponent)
                for wielden_weapon, (wielded, melee) in wielded_weapons:
                    if wielded.owner == entity and wielded.slot == EquipmentSlots.MELEE:
                        weapon_info = melee

                target_attributes = World.get_entity_component(wants_melee.target, AttributesComponent)
                target_skills = World.get_entity_component(wants_melee.target, SkillsComponent)

                # To hit calculation
                attacker_attribute_hit_bonus = 0
                if weapon_info:
                    if weapon_info.attribute == WeaponAttributes.MIGHT:
                        attacker_attribute_hit_bonus += attacker_attributes.might
                    elif weapon_info.attribute == WeaponAttributes.QUICKNESS:
                        attacker_attribute_hit_bonus += attacker_attributes.quickness

                attacker_skill_melee = skill_level(attacker_skill, Skills.MELEE)
                attacker_weapon_hit_bonus = 0
                modified_hit_roll = natural_roll + attacker_attribute_hit_bonus + \
                                    attacker_skill_melee + attacker_weapon_hit_bonus

                # Defense calculation
                dodge_quickness_bonus = target_attributes.quickness
                dodge_skill_dodge = skill_level(target_skills, Skills.DODGE)
                dodge_item_bonus = 0
                dodge_difficulty = dodge_quickness_bonus + dodge_skill_dodge + dodge_item_bonus

                # To Hit resolution
                if not natural_roll == 20 and not modified_hit_roll > dodge_difficulty:
                    # fail
                    logs.appendleft(f'{Texts.get_text("MISS_HIT").format(attacker_name.name, target_name)}')
                    World.remove_component(WantsToMeleeComponent, entity)
                    continue

                # success Damage calculation
                if weapon_info:
                    base_dmg = randint(weapon_info.min_dmg, weapon_info.max_dmg)
                    base_dmg += weapon_info.dmg_bonus
                else:
                    base_dmg = randint(config.DEFAULT_MIN_DMG, config.DEFAULT_MAX_DMG)
                attack_dmg = max(0, base_dmg + attacker_attributes.might + attacker_skill_melee)

                # armor mitigation calculation
                target_armor = target_attributes.body
                wearable_armors = World.get_components(EquippedComponent, WearableComponent)
                for wearable_armor, (equipped, wearable) in wearable_armors:
                    if equipped.owner == wants_melee.target:
                        target_armor += wearable.armor
                armor_roll = randint(0, target_armor)
                attack_dmg = max(0, attack_dmg - armor_roll)

                if attack_dmg:
                    attacker_is_player = False
                    if entity == World.fetch('player'):
                        attacker_is_player = True

                    logs.appendleft(
                        f'{Texts.get_text("HITS_FOR_DMG").format(attacker_name.name, target_name, attack_dmg)}')
                    target_suffer_dmg = SufferDamageComponent(attack_dmg, attacker_is_player)
                    World.add_component(target_suffer_dmg, wants_melee.target)
                else:
                    logs.appendleft(
                        f'{Texts.get_text("UNABLE_TO_HURT").format(attacker_name.name, target_name)}')
            World.remove_component(WantsToMeleeComponent, entity)
