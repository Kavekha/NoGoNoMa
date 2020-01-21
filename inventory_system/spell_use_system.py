from world import World
from systems.system import System
from components.intent_components import WantsToCastSpellComponent
from components.magic_item_components import IdentifiedItemComponent
from components.equip_components import EquipmentChangedComponent
from components.name_components import NameComponent
from components.area_effect_component import AreaOfEffectComponent
from effects.effects_system import add_effect, Effect, EffectType, Targets, TargetType
from effects.targeting_effect import get_aoe_tiles


class SpellUseSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToCastSpellComponent)
        player = World.fetch('player')

        for entity, (wants_to_cast, *args) in subjects:
            World.add_component(EquipmentChangedComponent(), entity)

            # identify
            spell_named = World.get_entity_component(wants_to_cast.spell, NameComponent)
            if entity == player and spell_named:
                World.add_component(IdentifiedItemComponent(name=spell_named.name), entity)

            # effect:
            if not wants_to_cast.target:
                target = Targets(TargetType.SINGLE, target=player)
            else:
                aoe = World.get_entity_component(wants_to_cast.spell, AreaOfEffectComponent)
                if aoe:
                    target = Targets(TargetType.TILES, tiles=get_aoe_tiles(wants_to_cast.target, aoe.radius))
                else:
                    current_map = World.fetch('current_map')
                    target_x, target_y = wants_to_cast.target
                    target = Targets(TargetType.TILE, tile=current_map.xy_idx(target_x,
                                                                              target_y))
            add_effect(entity, Effect(EffectType.SPELL_USE, spell=wants_to_cast.spell), target)

        World.remove_component_for_all_entities(WantsToCastSpellComponent)
