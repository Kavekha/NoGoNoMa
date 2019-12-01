from systems.system import System
from world import World
from components.wants_to_melee_component import WantsToMeleeComponent
from components.name_component import NameComponent
from components.combat_stats_component import CombatStatsComponent
from components.suffer_damage_component import SufferDamageComponent
from components.bonus_components import DefenseBonusComponent, PowerBonusComponent
from components.equipped_component import EquippedComponent
from texts import Texts


class MeleeCombatSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToMeleeComponent, NameComponent, CombatStatsComponent)
        if not subjects:
            return

        for entity, (wants_melee, name, combat_stats) in subjects:
            # Attacker Not dead
            if combat_stats.hp > 0:
                target_stats = World.get_entity_component(wants_melee.target, CombatStatsComponent)
                # Defenser not dead
                if target_stats.hp > 0:
                    # Calcul bonus / malus then dmg
                    offensive_bonus = 0
                    for _item_entity, (power_bonus, equipped_by) in World.get_components(PowerBonusComponent,
                                                                                         EquippedComponent):
                        if equipped_by.owner == entity:
                            offensive_bonus += power_bonus.power

                    defensive_bonus = 0
                    for _item_entity, (defense_bonus, equipped_by) in World.get_components(DefenseBonusComponent,
                                                                                           EquippedComponent):
                        if equipped_by.owner == wants_melee.target:
                            defensive_bonus += defense_bonus.defense

                    damage = max(0, (combat_stats.power + offensive_bonus) - (target_stats.defense + defensive_bonus))

                    # Logs
                    target_name = World.get_entity_component(wants_melee.target, NameComponent).name
                    logs = World.fetch('logs')
                    if damage == 0:
                        logs.appendleft(f'{Texts.get_text("UNABLE_TO_HURT").format(name.name, target_name)}')
                    else:
                        logs.appendleft(f'{Texts.get_text("HITS_FOR_DMG").format(name.name, target_name, damage)}')
                        target_suffer_dmg = SufferDamageComponent(damage)
                        World.add_component(target_suffer_dmg, wants_melee.target)

            World.remove_component(WantsToMeleeComponent, entity)