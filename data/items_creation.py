from components.item_component import ItemComponent
from components.provides_healing_component import ProvidesHealingComponent
from components.consumable_component import ConsumableComponent
from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent
from components.name_component import NameComponent
from components.ranged_component import RangedComponent
from components.inflicts_damage_component import InflictsDamageComponent

from data.types import Layers
from world import World


def create_healing_potion_item(x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent('!', 'purple', Layers.ITEM)
    name = NameComponent('Health Potion')
    item = ItemComponent()
    consumable = ConsumableComponent()
    provide_healing = ProvidesHealingComponent(amount=8)
    item_id = World.create_entity(position, renderable, name, item, provide_healing, consumable)
    return item_id


def create_magic_missile_scroll(x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent(')', 'cyan', Layers.ITEM)
    name = NameComponent('Magic missile scroll')
    item = ItemComponent()
    consumable = ConsumableComponent()
    ranged = RangedComponent(6)
    inflicts_damage = InflictsDamageComponent(8)
    item_id = World.create_entity(position, renderable, name, item, ranged, inflicts_damage, consumable)
    return item_id
