from random import randint

from systems.system import System
from components.initiative import InitiativeComponent, MyTurn
from components.position_component import PositionComponent
from components.name_component import NameComponent
from world import World
from state import States
import config


class InitiativeSystem(System):
    def update(self, *args, **kwargs):
        run_state = World.fetch('state')
        if run_state.current_state != States.TICKING:
            return

        # on s'assure qu'i n'y a plus de "My Turn".
        World.remove_component_for_all_entities(MyTurn)
        subjects = World.get_components(InitiativeComponent, PositionComponent)

        for entity, (initiative, position) in subjects:
            initiative.current -= config.DEFAULT_INITIATIVE_TICK
            if initiative.current < 1:
                World.add_component(MyTurn(), entity)
                initiative.current += config.DEFAULT_INITIATIVE_GAIN

                # Here go any Malus / Bonus for initiative. Or initiative action cost?

                if entity == World.fetch('player'):
                    run_state.change_state(States.AWAITING_INPUT)
