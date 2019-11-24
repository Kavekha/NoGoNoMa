from systems.system import System
from components.wants_use_item_component import WantsToUseComponent
from components.combat_stats_component import CombatStatsComponent
from components.provides_healing_component import ProvidesHealingComponent
from components.inflicts_damage_component import InflictsDamageComponent
from components.name_component import NameComponent
from components.consumable_component import ConsumableComponent
from components.suffer_damage_component import SufferDamageComponent
from gmap.utils import xy_idx
from world import World
import config


class ItemUseSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantsToUseComponent, CombatStatsComponent)
        if not subjects:
            return

        player = World.fetch('player')
        logs = World.fetch('logs')
        for entity, (wants_to_use, stats, *args) in subjects:
            item_inflicts_dmg = World.get_entity_component(wants_to_use.item, InflictsDamageComponent)
            item_provides_healing = World.get_entity_component(wants_to_use.item, ProvidesHealingComponent)
            item_name = World.get_entity_component(wants_to_use.item, NameComponent)

            if item_provides_healing:
                stats.hp = min(stats.max_hp, stats.hp + item_provides_healing.healing_amount)
                if entity == player:
                    logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]You drink: {item_name.name}'
                                    f' You are heal for {item_provides_healing.healing_amount} hp.[/color]')

            if item_inflicts_dmg:
                target_x, target_y = wants_to_use.target
                idx = xy_idx(target_x, target_y)
                current_map = World.fetch('current_map')
                for mob in current_map.tile_content[idx]:
                    suffer_dmg = SufferDamageComponent(item_inflicts_dmg.damage)
                    World.add_component(suffer_dmg, mob)
                    if entity == player:
                        mob_name = World.get_entity_component(mob, NameComponent)
                        logs.appendleft(f'[color={config.COLOR_PLAYER_INFO_OK}] '
                                        f'You use {item_name.name} on {mob_name.name}'
                                        f' for {item_inflicts_dmg.damage} hp.')

            consumable = World.get_entity_component(wants_to_use.item, ConsumableComponent)
            if consumable:
                World.delete_entity(wants_to_use.item)

            World.remove_component(WantsToUseComponent, entity)
