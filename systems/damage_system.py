from systems.system import System
from world import World
from components.combat_stats_component import CombatStatsComponent
from components.suffer_damage_component import SufferDamageComponent
from components.name_component import NameComponent


class DamageSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(SufferDamageComponent, CombatStatsComponent, NameComponent)
        if not subjects:
            return

        for entity, (suffer_damage, combat_stats, name) in subjects:
            combat_stats.hp -= suffer_damage.amount
            print(f'{name.name} has been damage for {suffer_damage.amount}. {combat_stats.hp} remaining')
            World.remove_component(SufferDamageComponent, entity)
