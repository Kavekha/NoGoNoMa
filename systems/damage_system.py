from random import randint

from systems.system import System
from world import World
import config
from components.pools_component import Pools
from components.suffer_damage_component import SufferDamageComponent
from components.name_component import NameComponent
from components.position_component import PositionComponent
from player_systems.game_system import player_gain_xp, calculate_xp_from_entity
from player_systems.on_death import on_player_death
from texts import Texts
from gmap.utils import xy_idx


class DamageSystem(System):
    def update(self, *args, **kwargs):
        subjects = World.get_components(SufferDamageComponent, Pools, NameComponent)

        player = World.fetch('player')
        logs = World.fetch('logs')

        for entity, (suffer_damage, pools, name) in subjects:
            pools.hit_points.current -= suffer_damage.amount

            if randint(1, 100) >= config.BLOOD_ON_GROUND_CHANCE:
                pos = World.get_entity_component(entity, PositionComponent)
                current_map = World.fetch('current_map')
                current_map.stains[xy_idx(pos.x, pos.y)] = randint(1, 5)

            if pools.hit_points.current < 1:
                if entity != player:
                    logs.appendleft(f'[color={config.COLOR_MAJOR_INFO}]'
                                    f'{Texts.get_text("_HAS_BEEN_SLAIN").format(Texts.get_text(name.name))}[/color]')
                    if suffer_damage.from_player:
                        player_gain_xp(calculate_xp_from_entity(entity))
                    World.delete_entity(entity)
                else:
                    on_player_death()

            World.remove_component(SufferDamageComponent, entity)
