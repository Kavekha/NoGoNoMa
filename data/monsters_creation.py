'''
from components.monster_component import MonsterComponent
from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent
from components.viewshed_component import ViewshedComponent
from components.name_component import NameComponent
from components.blocktile_component import BlockTileComponent
from components.combat_stats_component import CombatStatsComponent
from ui_system.ui_enums import Layers
from world import World


# Generique
def create_monster(name, x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent('g', 'red', Layers.MONSTER)
    name = NameComponent(name)
    viewshed = ViewshedComponent(8)
    block = BlockTileComponent()
    monster_component = MonsterComponent()
    combat_stats = CombatStatsComponent(16, 1, 4)
    monster_id = World.create_entity(position, renderable, viewshed, name, monster_component, block, combat_stats)
    return monster_id


def create_monster_morblin(x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent('m', 'light green', Layers.MONSTER)
    name = NameComponent('Morblin')
    viewshed = ViewshedComponent(6)
    block = BlockTileComponent()
    monster_component = MonsterComponent()
    combat_stats = CombatStatsComponent(hp=12, defense=1, power=4)
    monster_id = World.create_entity(position, renderable, viewshed, name, monster_component, block, combat_stats)
    return monster_id


def create_monster_orcish(x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent('o', 'light red', Layers.MONSTER)
    name = NameComponent('Orcish')
    viewshed = ViewshedComponent(6)
    block = BlockTileComponent()
    monster_component = MonsterComponent()
    combat_stats = CombatStatsComponent(hp=18, defense=2, power=5)
    monster_id = World.create_entity(position, renderable, viewshed, name, monster_component, block, combat_stats)
    return monster_id
'''