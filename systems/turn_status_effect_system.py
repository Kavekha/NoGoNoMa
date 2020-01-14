from systems.system import System
from components.initiative_components import MyTurn, InitiativeCostComponent
from components.status_effect_components import StatusEffectComponent, ConfusionComponent, DurationComponent
from components.equip_components import EquipmentChangedComponent
from world import World
from state import States
import config


class TurnStatusEffectSystem(System):
    def update(self, *args, **kwargs):
        """Time is relative, so 'A turn' is any time it's the player turn.
        A bit unfair, since the quicker he is, the quicker the effect worns off
        other possibility : InitiativeCostComponent, that increase Initiative.

        Note: A StatusEffect is an entity, with following components:
        - StatusEffect (with target containing the entity affected)
        - Duration (how many turns)
        - The effect applyied on the target
        """

        run_state = World.fetch('state')
        if run_state.current_state != States.TICKING:
            return

        entities_turn = list()
        subjects = World.get_components(MyTurn)

        for entity, (_turn, *args) in subjects:
            entities_turn.append(entity)

        entities_under_confusion_at_duration_tick = list()  # entities that have a confusion effect
        entities_and_components_effects_applied_this_update = list()

        # find entity affected by status_effect
        statuses = World.get_components(StatusEffectComponent)
        for effect, (status, *args) in statuses:
            print(f'turn status effect: entities turn is {entities_turn} and status target is {status.target}')
            if status.target in entities_turn:
                entities_and_components_effects_applied_this_update.append((effect, status))
                # Its entity turn and it have a status effect
                # confusion
                confusion = World.get_entity_component(effect, ConfusionComponent)
                if confusion:
                    entities_under_confusion_at_duration_tick.append(status.target)

        # effect applied
        for entity in entities_under_confusion_at_duration_tick:
            # lost its turn and wait X initiative after that.
            World.remove_component(MyTurn, entity)
            World.add_component(InitiativeCostComponent(config.DEFAULT_CONFUSION_INITIATIVE_COST), entity)

        # Effect has act this turn, so it worns off.
        effects_ended = list()
        for effect_entity, effect_status in entities_and_components_effects_applied_this_update:
            duration = World.get_entity_component(effect_entity, DurationComponent)
            duration.turns -= 1
            if duration.turns < 1:
                World.add_component(EquipmentChangedComponent(), effect_status.target)  # dirty, so recalculate things
                effects_ended.append(effect_entity)

        print(f'effects ended is {effects_ended}')
        for effect_ended in effects_ended:
            World.delete_entity(effect_ended)
