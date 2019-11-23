from systems.system import System
from world import World
from components.combat_stats_component import CombatStatsComponent
from components.name_component import NameComponent
import config


class DeathSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(CombatStatsComponent, NameComponent)
        if not subjects:
            return

        player = World.fetch('player')
        for entity, (combat_stats, name, *args) in subjects:
            logs = World.fetch('logs')
            if combat_stats.hp < 1:
                if entity != player:
                    logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]{name.name} has been slain.[/color]')
                    World.delete_entity(entity)
                else:
                    print(f'You are dead!')
                    logs.appendleft(f'[color={config.COLOR_DEADLY_INFO}]You are dead![/color]')
