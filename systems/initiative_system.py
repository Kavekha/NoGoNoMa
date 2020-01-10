from systems.system import System
from components.initiative_components import InitiativeComponent, MyTurn, InitiativeCostComponent
from components.position_components import PositionComponent
from map_builders.commons import distance_to
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

        player = World.fetch('player')
        player_pos = World.get_entity_component(player, PositionComponent)
        subjects = World.get_components(InitiativeComponent, PositionComponent)
        # subjects = sorted(subjects, key=lambda entry: entry[1][0].current)

        for entity, (initiative, position) in subjects:
            print(f'INITIATIVE: {entity} initiative is : {initiative.current}')

            initiative_cost = World.get_entity_component(entity, InitiativeCostComponent)
            if initiative_cost:
                initiative.current += initiative_cost.cost
                World.remove_component(InitiativeCostComponent, entity)
            else:
                if entity != player and distance_to(player_pos.x, player_pos.y, position.x, position.y) > config.MIN_DISTANCE_TO_BE_ACTIVE:
                    print(f'INITIATIVE: {entity} is not active. Initiative is : {initiative.current}')
                    continue

                print(f'INITIATIVE: {entity} is active, with : {initiative.current}')

                initiative.current -= config.DEFAULT_INITIATIVE_TICK
                if initiative.current < 1:
                    # Cas 2: I dont have an InitiativeCost. I must do something.
                    World.add_component(MyTurn(), entity)

                    if entity == World.fetch('player'):
                        run_state.change_state(States.AWAITING_INPUT)
