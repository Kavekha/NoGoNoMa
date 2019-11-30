from bearlibterminal import terminal

from systems.system import System
from world import World
import config
from components.combat_stats_component import CombatStatsComponent
from components.suffer_damage_component import SufferDamageComponent
from components.name_component import NameComponent
from data.types import States


class DamageSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(SufferDamageComponent, CombatStatsComponent, NameComponent)
        if not subjects:
            return

        player = World.fetch('player')
        logs = World.fetch('logs')

        for entity, (suffer_damage, combat_stats, name) in subjects:
            combat_stats.hp -= suffer_damage.amount
            print(f'{name.name} has been damage for {suffer_damage.amount}. {combat_stats.hp} remaining')
            World.remove_component(SufferDamageComponent, entity)

            if combat_stats.hp < 1:
                if entity != player:
                    logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]{name.name} has been slain.[/color]')
                    World.delete_entity(entity)
                else:
                    print(f'You are dead!')
                    logs.appendleft(f'[color={config.COLOR_DEADLY_INFO}]You are dead![/color]')
                    run_state = World.fetch('state')
                    run_state.change_state(States.GAME_OVER)
                    World.insert('state', run_state)
