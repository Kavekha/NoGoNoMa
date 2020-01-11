from random import randint

from systems.system import System
from components.initiative_components import InitiativeComponent, MyTurn, InitiativeCostComponent
from components.position_components import PositionComponent
from components.name_components import NameComponent
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

        # sorting initiative
        subjects = World.get_components(InitiativeComponent, PositionComponent)
        # subjects = sorted(subjects, key=lambda entry: entry[1][0].current)

        for entity, (initiative, position) in subjects:
            print(f'entity {entity} with initiative of {initiative.current}')
            # Cas 1: I have an initiativeCost: I've done something and my initiative need to be updated.
            initiative_cost = World.get_entity_component(entity, InitiativeCostComponent)
            if initiative_cost:
                # initiative.current += randint(1, config.DEFAULT_INITIATIVE_GAIN)
                initiative.current += initiative_cost.cost
                # Here go any Malus / Bonus for initiative. Or initiative action cost?
                World.remove_component(InitiativeCostComponent, entity)
            else:
                # if no cost, then no action: let's reduce my initiative and see if its my turn:
                # !NOTA: if we do initiative.cost then initiative.Current - 1, we risk to get in a unending loop.
                initiative.current -= config.DEFAULT_INITIATIVE_TICK
                if initiative.current < 1:
                    # Cas 2: I dont have an InitiativeCost. I must do something.
                    World.add_component(MyTurn(), entity)

                    if entity == World.fetch('player'):
                        run_state.change_state(States.AWAITING_INPUT)
