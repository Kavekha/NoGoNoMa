from systems.system import System
from components.wants_use_item_component import WantsToUseComponent
from components.combat_stats_component import CombatStatsComponent
from components.provides_healing_component import ProvidesHealingComponent
from components.name_component import NameComponent
from components.consumable_component import ConsumableComponent
from world import World
import config


class ItemUseSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToUseComponent, CombatStatsComponent)
        if not subjects:
            return

        player = World.fetch('player')
        logs = World.fetch('logs')
        for entity, (wants_to_drink, stats, *args) in subjects:
            item = World.get_entity_component(wants_to_drink.item, ProvidesHealingComponent)
            item_name = World.get_entity_component(wants_to_drink.item, NameComponent)
            if item:
                stats.hp = min(stats.max_hp, stats.hp + item.healing_amount)
                if entity == player:
                    logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]You drink: {item_name.name}'
                                    f' You are heal for {item.healing_amount} hp.[/color]')
                consumable = World.get_entity_component(wants_to_drink.item, ConsumableComponent)
                if consumable:
                    World.delete_entity(wants_to_drink.item)
            World.remove_component(WantsToUseComponent, entity)
