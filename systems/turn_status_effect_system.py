from systems.system import System
from components.initiative_components import MyTurn, InitiativeCostComponent
from components.status_effect_components import StatusEffectComponent, ConfusionComponent, DurationComponent
from components.equip_components import EquipmentChangedComponent
from components.name_components import NameComponent
from world import World
from state import States
import config
from texts import Texts


class TurnStatusEffectSystem(System):
    def update(self, *args, **kwargs):
        """Time is relative, so 'A turn' is any time it's the char turn. No "Universal Turn" exists.

        Note: A StatusEffect is an entity, with following components:
        - StatusEffect (with target containing the entity affected)
        - Duration (how many turns)
        - The effect applyied on the target
        """

        # On recupere les entities qui joueront ce tour.
        entities_turn = list()
        subjects = World.get_components(MyTurn)
        for entity, (_turn, *args) in subjects:
            entities_turn.append(entity)
        print(f'turn status effect: Turn for: {entities_turn}')

        # On se prepare à enregistrer les entités dont c'est le tour et qui ont un effet sur eux
        entities_under_confusion_at_duration_tick = list()  # entities that have a confusion effect
        entities_and_components_effects_applied_this_update = list()

        # On recupere les entités "StatusEffect" qui contiennent leur victime
        statuses = World.get_components(StatusEffectComponent)
        for effect_entity, (status, *args) in statuses:
            if status.target in entities_turn:
                entities_and_components_effects_applied_this_update.append((effect_entity, status))
                # Its entity turn and it have a status effect
                # Effect that will have to apply
                # confusion
                confusion = World.get_entity_component(effect_entity, ConfusionComponent)
                if confusion:
                    entities_under_confusion_at_duration_tick.append(status.target)

        run_state = World.fetch('state')
        # Si c'est Ticking, c'est pour les mobs.
        # Si c'est Player has MyTurn, c'est pour le joueur.
        # Si pas ticking, alors probablement Menu ou Waiting For Input: pas de raison que ca tourne.
        if run_state.current_state == States.TICKING or World.get_entity_component(World.fetch('player'), MyTurn):
            logs = World.fetch('logs')

            # effect applied on victims
            # confusion
            for entity in entities_under_confusion_at_duration_tick:
                # lost its turn and wait X initiative after that.
                World.remove_component(MyTurn, entity)  # perd son tour.
                # augmente le temps avant prochain tour.
                World.add_component(InitiativeCostComponent(config.DEFAULT_CONFUSION_INITIATIVE_COST), entity)
                # if player:
                if entity == World.fetch('player'):
                    run_state = run_state.change_state(States.TICKING)

            # Effect has act this turn, so it worns off.
            effects_ended = list()
            for effect_entity, effect_status in entities_and_components_effects_applied_this_update:
                duration = World.get_entity_component(effect_entity, DurationComponent)
                duration.turns -= 1
                if duration.turns < 1:
                    World.add_component(EquipmentChangedComponent(), effect_status.target)  # dirty, so recalculate things
                    effects_ended.append(effect_entity)

            for effect_ended in effects_ended:
                effect_name = World.get_entity_component(effect_ended, NameComponent).name
                effect_target = World.get_entity_component(effect_ended, StatusEffectComponent).target
                target_name = World.get_entity_component(effect_target, NameComponent).name
                if effect_name and effect_target:
                    logs.appendleft(f'{effect_name}{Texts.get_text("_EFFECT_FADES_ON_")}{target_name}')

                World.delete_entity(effect_ended)
