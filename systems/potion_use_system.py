from systems.system import System
from components.wants_to_drink_potion_component import WantToDrinkPotionComponent
from components.combat_stats_component import CombatStatsComponent
from components.potion_component import PotionComponent
from components.name_component import NameComponent
from world import World
import config


class PotionUseSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(WantToDrinkPotionComponent, CombatStatsComponent)
        if not subjects:
            return

        player = World.fetch('player')
        logs = World.fetch('logs')
        for entity, (wants_to_drink, stats, *args) in subjects:
            potion = World.get_entity_component(wants_to_drink.potion, PotionComponent)
            potion_name = World.get_entity_component(wants_to_drink.potion, NameComponent)
            if potion:
                stats.hp = min(stats.max_hp, stats.hp + potion.amount)
                if entity == player:
                    logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]You drink {potion_name.name},'
                                    f' healing {potion.amount} hp.[/color]')
                World.delete_entity(wants_to_drink.potion)
            World.remove_component(WantToDrinkPotionComponent, entity)
