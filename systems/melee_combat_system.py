from systems.system import System
from world import World
from components.wants_to_melee_component import WantsToMeleeComponent
from components.name_component import NameComponent
from components.combat_stats_component import CombatStatsComponent
from components.suffer_damage_component import SufferDamageComponent


class MeleeCombatSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToMeleeComponent, NameComponent, CombatStatsComponent)
        if not subjects:
            return

        for entity, (wants_melee, name, combat_stats) in subjects:
            # Not dead
            if combat_stats.hp > 0:
                target_stats = World.get_entity_component(wants_melee.target, CombatStatsComponent)
                if target_stats.hp > 0:
                    target_name = World.get_entity_component(wants_melee.target, NameComponent).name
                    damage = max(0, combat_stats.power - target_stats.defense)
                    logs = World.fetch('logs')
                    if damage == 0:
                        logs.appendleft(f'{target_name} is unable to hurt {name.name}')
                        print(f'{target_name} is unable to hurt {name.name}')
                    else:
                        logs.appendleft(f'{name.name} hits {target_name} for {damage} hp.')
                        print(f'{name.name} hits {target_name} for {damage} hp.')
                        target_suffer_dmg = SufferDamageComponent(damage)
                        World.add_component(target_suffer_dmg, wants_melee.target)
            World.remove_component(WantsToMeleeComponent, entity)