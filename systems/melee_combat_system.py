from random import randint

from systems.system import System
from world import World
from components.wants_to_melee_component import WantsToMeleeComponent
from components.name_component import NameComponent
from components.pools_component import Pools
from components.attributes_component import AttributesComponent
from components.suffer_damage_component import SufferDamageComponent
from components.bonus_components import DefenseBonusComponent, PowerBonusComponent
from components.equipped_component import EquippedComponent
from components.skills_component import SkillsComponent, Skills
from systems.game_system import skill_level
from texts import Texts


class MeleeCombatSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToMeleeComponent, NameComponent, Pools, AttributesComponent)
        if not subjects:
            return

        for entity, (wants_melee, attacker_name, attacker_pools, attacker_attributes) in subjects:
            # Attacker Not dead
            if attacker_pools.hit_points.current > 0:
                target_pools = World.get_entity_component(wants_melee.target, Pools)
                # Defenser not dead
                print(f'melee combat: target is {wants_melee.target}, pool is {target_pools}')
                if target_pools.hit_points.current > 0:
                    target_attributes = World.get_entity_component(wants_melee.target, AttributesComponent)
                    target_skills = World.get_entity_component(wants_melee.target, SkillsComponent)
                    attacker_skill = World.get_entity_component(entity, SkillsComponent)

                    natural_roll = randint(1, 20)
                    attacker_attribute_might = attacker_attributes.might
                    attacker_skill_melee = skill_level(attacker_skill, Skills.MELEE)
                    attacker_weapon_hit_bonus = 0
                    modified_hit_roll = natural_roll + attacker_attribute_might + \
                                        attacker_skill_melee + attacker_weapon_hit_bonus

                    target_name = World.get_entity_component(wants_melee.target, NameComponent).name
                    armor_quickness_bonus = target_attributes.quickness
                    armor_skill_defense = skill_level(target_skills, Skills.DEFENSE)
                    armor_item_bonus = 0
                    armor_class = armor_quickness_bonus + armor_skill_defense + armor_item_bonus
                    print(f'target is {target_name}, quick {armor_quickness_bonus}, skill def {armor_skill_defense}')

                    attack_dmg = 0
                    # Logs
                    target_name = World.get_entity_component(wants_melee.target, NameComponent).name
                    logs = World.fetch('logs')

                    print(f'natural roll is {natural_roll} and armor class is {armor_class}')
                    if natural_roll != 1 and (natural_roll == 20 or modified_hit_roll > armor_class):
                        # Attacker hit
                        base_dmg = randint(1, 4)
                        weapon_dmg_bonus = 0
                        attack_dmg = max(0, base_dmg + attacker_attributes.might + attacker_skill_melee +
                                         weapon_dmg_bonus)

                        if attack_dmg:
                            logs.appendleft(
                                f'{Texts.get_text("HITS_FOR_DMG").format(attacker_name.name, target_name, attack_dmg)}')
                            target_suffer_dmg = SufferDamageComponent(attack_dmg)
                            World.add_component(target_suffer_dmg, wants_melee.target)
                        else:
                            logs.appendleft(
                                f'{Texts.get_text("UNABLE_TO_HURT").format(attacker_name.name, target_name)}')

                    elif natural_roll == 1:
                        logs.appendleft(f'{Texts.get_text("FAIL_TO_HIT").format(attacker_name.name, target_name)}')
                    else:
                        logs.appendleft(f'{Texts.get_text("MISS_HIT").format(attacker_name.name, target_name, attack_dmg)}')

            World.remove_component(WantsToMeleeComponent, entity)
