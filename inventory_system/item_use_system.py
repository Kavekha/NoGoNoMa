from world import World
from systems.system import System
from components.intent_components import WantsToUseComponent
from components.magic_item_components import IdentifiedItemComponent
from components.name_components import NameComponent
from components.area_effect_component import AreaOfEffectComponent
from effects.effects_system import add_effect, Effect, EffectType, Targets, TargetType, get_aoe_tiles


class ItemUseSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToUseComponent)
        player = World.fetch('player')

        for entity, (wants_to_use, *args) in subjects:
            print(f'ITEM USE SYSTEM for {entity}')
            # identify
            item_named = World.get_entity_component(wants_to_use.item, NameComponent)
            if entity == player:
                World.add_component(IdentifiedItemComponent(name=item_named.name), wants_to_use.item)

            # effect:
            if not wants_to_use.target:
                target = Targets(TargetType.SINGLE, target=player)
            else:
                aoe = World.get_entity_component(wants_to_use.item, AreaOfEffectComponent)
                if aoe:
                    target = Targets(TargetType.TILES, tiles=get_aoe_tiles(wants_to_use.target, aoe.radius))
                else:
                    current_map = World.fetch('current_map')
                    target = Targets(TargetType.TILE, tile=current_map.xy_idx(wants_to_use.target.x,
                                                                              wants_to_use.target.y))

            add_effect(entity, Effect(EffectType.ITEM_USE, item=wants_to_use.item), target)

        World.remove_component_for_all_entities(WantsToUseComponent)
