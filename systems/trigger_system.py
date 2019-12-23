from systems.system import System
from world import World
from components.triggers_components import EntityMovedComponent, EntryTriggerComponent, ActivationComponent
from components.position_component import PositionComponent
from components.hidden_component import HiddenComponent
from components.inflicts_damage_component import InflictsDamageComponent
from components.suffer_damage_component import SufferDamageComponent
from components.skills_component import Skills
from ui_system.render_functions import get_obfuscate_name
from systems.particule_system import ParticuleBuilder
from player_systems.game_system import skill_roll_against_difficulty
from texts import Texts
import config


class TriggerSystem(System):
    def update(self, *args, **kwargs):
        print(f'TRIGGER: update')
        subjects = World.get_components(EntityMovedComponent, PositionComponent)
        current_map = World.fetch('current_map')
        remove_entities = []
        for entity, (has_moved, position, *args) in subjects:
            idx = current_map.xy_idx(position.x, position.y)
            for entity_id in current_map.tile_content[idx]:
                if entity is not entity_id:
                    print(f'entity {entity} is not {entity_id}')
                    maybe_trigger = World.get_entity_component(entity_id, EntryTriggerComponent)
                    print(f'entity id {entity_id} has maybe a trigger : {maybe_trigger}')
                    if not maybe_trigger:
                        continue
                    else:
                        # Triggering!
                        logs = World.fetch('logs')
                        entity_id_name = get_obfuscate_name(entity_id)
                        if entity_id_name:
                            final_log_trigger = Texts.get_text("SOMETHING_TRIGGERS")
                        else:
                            final_log_trigger = Texts.get_text("_TRIGGERS")

                        # Dodge effect!
                        if skill_roll_against_difficulty(entity, Skills.FOUND_TRAPS, config.DEFAULT_TRAP_DODGE):
                            final_log_consequence = Texts.get_text('YOU_DODGE_IT')

                        else:
                            # effects werent dodge
                            final_log_consequence = Texts.get_text('IT_HITS_YOU')
                            logs.appendleft(f"[color={config.COLOR_MAJOR_INFO}]"
                                            f"{final_log_trigger}{final_log_consequence}"
                                            f"[/color]")

                            inflict_dmg = World.get_entity_component(entity_id, InflictsDamageComponent)
                            if inflict_dmg:
                                print(f'trigger: inflict dmg : {inflict_dmg} with dmg : {inflict_dmg.damage}')
                                ParticuleBuilder.request(position.x, position.y,
                                                         config.COLOR_PARTICULE_HIT, '!!', 'particules/attack.png')
                                suffer_dmg = SufferDamageComponent(inflict_dmg.damage, from_player=False)
                                World.add_component(suffer_dmg, entity)

                        activation = World.get_entity_component(entity_id, ActivationComponent)
                        if activation:
                            activation.nb_activations -= 1
                            if not activation.nb_activations:
                                remove_entities.append(entity_id)

                        hidden = World.get_entity_component(entity_id, HiddenComponent)
                        if hidden:
                            World.remove_component(hidden, entity_id)

        World.remove_component_for_all_entities(EntityMovedComponent)
        for entity in remove_entities:
            World.delete_entity(entity)
