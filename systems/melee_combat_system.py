from systems.system import System
from world import World
from components.wants_to_melee_component import WantsToMeleeComponent
from components.name_component import NameComponent
from components.pools_component import Pools
from components.attributes_component import AttributesComponent
from components.suffer_damage_component import SufferDamageComponent
from components.bonus_components import DefenseBonusComponent, PowerBonusComponent
from components.equipped_component import EquippedComponent
from texts import Texts


class MeleeCombatSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToMeleeComponent, NameComponent, Pools, AttributesComponent)
        if not subjects:
            return

        for entity, (wants_melee, name, pools, attributes) in subjects:
            # Attacker Not dead
            if pools.hit_points.current > 0:
                target_pools = World.get_entity_component(wants_melee.target, Pools)
                # Defenser not dead
                print(f'melee combat: target is {wants_melee.target}, pool is {target_pools}')
                if target_pools.hit_points.current > 0:
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

                    target_attributes = World.get_entity_component(wants_melee.target, AttributesComponent)
                    damage = max(0, (attributes.might + offensive_bonus) - (target_attributes.body + defensive_bonus))

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
