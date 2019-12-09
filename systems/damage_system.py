from systems.system import System
from world import World
import config
from components.pools_component import Pools
from components.suffer_damage_component import SufferDamageComponent
from components.name_component import NameComponent
from state import States
from texts import Texts


class DamageSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(SufferDamageComponent, Pools, NameComponent)
        if not subjects:
            return

        player = World.fetch('player')
        logs = World.fetch('logs')

        for entity, (suffer_damage, pools, name) in subjects:
            pools.hit_points.current -= suffer_damage.amount
            World.remove_component(SufferDamageComponent, entity)

            if pools.hit_points.current < 1:
                if entity != player:
                    logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]'
                                    f'{Texts.get_text("_HAS_BEEN_SLAIN").format(name.name)}[/color]')
                    World.delete_entity(entity)
                else:
                    print(f'You are dead!')
                    logs.appendleft(f'[color={config.COLOR_DEADLY_INFO}]{Texts.get_text("YOU_ARE_DEAD")}[/color]')
                    run_state = World.fetch('state')
                    run_state.change_state(States.GAME_OVER)
                    World.insert('state', run_state)
