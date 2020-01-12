from systems.system import System
from world import World
from components.triggers_components import EntryTriggerComponent
from components.position_components import PositionComponent, EntityMovedComponent
from components.area_effect_component import AreaOfEffectComponent
from components.skills_component import Skills
from ui_system.render_functions import get_obfuscate_name
from player_systems.game_system import skill_roll_against_difficulty
from effects.effects_system import add_effect, Targets, TargetType, EffectType, Effect, get_aoe_tiles, entity_position
from texts import Texts
import config


class TriggerSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(EntityMovedComponent, PositionComponent)
        current_map = World.fetch('current_map')
        remove_entities = []

        for entity, (has_moved, position, *args) in subjects:
            idx = current_map.xy_idx(position.x, position.y)
            for entity_id in current_map.tile_content[idx]:
                if entity is not entity_id:
                    maybe_trigger = World.get_entity_component(entity_id, EntryTriggerComponent)
                    if not maybe_trigger:
                        continue
                    else:
                        # Triggering!
                        logs = World.fetch('logs')
                        entity_id_name = get_obfuscate_name(entity_id)
                        if entity_id_name:
                            final_log_trigger = Texts.get_text("_TRIGGERS").format(Texts.get_text(entity_id_name))
                        else:
                            final_log_trigger = Texts.get_text("SOMETHING_TRIGGERS")

                        # Dodge effect!
                        if skill_roll_against_difficulty(entity, Skills.FOUND_TRAPS, config.DEFAULT_TRAP_DODGE):
                            final_log_consequence = Texts.get_text('YOU_DODGE_IT')

                        else:
                            # effects werent dodge
                            final_log_consequence = Texts.get_text('IT_HITS_YOU')
                            aoe_component = World.get_entity_component(entity_id, AreaOfEffectComponent)
                            if aoe_component:
                                target = Targets(TargetType.TILES,
                                                 tiles=get_aoe_tiles(current_map.xy_idx(position.x, position.y),
                                                                     aoe_component.radius))
                            else:
                                target = Targets(TargetType.TILE, tile=entity_position(entity))
                            add_effect(entity_id, Effect(EffectType.TRIGGER_FIRE, trigger=entity_id), target)

                            """

                            inflict_dmg = World.get_entity_component(entity_id, InflictsDamageComponent)
                            if inflict_dmg:
                                ParticuleBuilder.request(position.x, position.y,
                                                         config.COLOR_PARTICULE_HIT, '!!', 'particules/attack.png')
                                suffer_dmg = SufferDamageComponent(inflict_dmg.damage, from_player=False)
                                World.add_component(suffer_dmg, entity)
                            
                            """
                        logs.appendleft(f"[color={config.COLOR_MAJOR_INFO}]"
                                        f"{final_log_trigger} {final_log_consequence}"
                                        f"[/color]")

                        """
                        activation = World.get_entity_component(entity_id, ActivationComponent)
                        if activation:
                            activation.nb_activations -= 1
                            if not activation.nb_activations:
                                remove_entities.append(entity_id)

                        hidden = World.get_entity_component(entity_id, HiddenComponent)
                        if hidden:
                            World.remove_component(hidden, entity_id)
                        """

        World.remove_component_for_all_entities(EntityMovedComponent)
        for entity in remove_entities:
            World.delete_entity(entity)
