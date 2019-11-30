from components.item_component import ItemComponent
from components.provides_healing_component import ProvidesHealingComponent
from components.consumable_component import ConsumableComponent
from components.position_component import PositionComponent
from components.renderable_component import RenderableComponent
from components.name_component import NameComponent
from components.ranged_component import RangedComponent
from components.inflicts_damage_component import InflictsDamageComponent
from components.area_effect_component import AreaOfEffectComponent
from components.confusion_component import ConfusionComponent
from components.equippable_component import EquippableComponent
from components.bonus_components import PowerBonusComponent, DefenseBonusComponent

from data.types import Layers, EquipmentSlots
from world import World
import config


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


def create_fireball_scroll(x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent(')', 'orange', Layers.ITEM)
    name = NameComponent('Fireball scroll')
    item = ItemComponent()
    consumable = ConsumableComponent()
    ranged = RangedComponent(6)
    inflicts_damage = InflictsDamageComponent(20)
    area_of_effect = AreaOfEffectComponent(config.LOW_RADIUS)
    item_id = World.create_entity(position, renderable, name, item, ranged, inflicts_damage, consumable, area_of_effect)
    return item_id


def create_confusion_scroll(x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent(')', 'pink', Layers.ITEM)
    name = NameComponent('Confusion scroll')
    item = ItemComponent()
    consumable = ConsumableComponent()
    ranged = RangedComponent(6)
    confusion = ConfusionComponent(4)
    item_id = World.create_entity(position, renderable, name, item, ranged, confusion, consumable)
    return item_id


def create_dagger(x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent('/', 'dark cyan', Layers.ITEM)
    name = NameComponent('Dagger')
    item = ItemComponent()
    equippable = EquippableComponent(EquipmentSlots.MELEE)
    power_bonus = PowerBonusComponent(2)
    item_id = World.create_entity(position, renderable, name, item, equippable, power_bonus)
    return item_id


def create_shield(x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent('[[', 'dark cyan', Layers.ITEM)
    name = NameComponent('Shield')
    item = ItemComponent()
    equippable = EquippableComponent(EquipmentSlots.SHIELD)
    defense_bonus = DefenseBonusComponent(1)
    item_id = World.create_entity(position, renderable, name, item, equippable, defense_bonus)
    return item_id


def create_long_sword(x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent('/', 'light blue', Layers.ITEM)
    name = NameComponent('Long sword')
    item = ItemComponent()
    equippable = EquippableComponent(EquipmentSlots.MELEE)
    power_bonus = PowerBonusComponent(4)
    item_id = World.create_entity(position, renderable, name, item, equippable, power_bonus)
    return item_id


def create_tower_shield(x, y):
    position = PositionComponent(x, y)
    renderable = RenderableComponent('[[', 'light blue', Layers.ITEM)
    name = NameComponent('Tower shield')
    item = ItemComponent()
    equippable = EquippableComponent(EquipmentSlots.SHIELD)
    defense_bonus = DefenseBonusComponent(2)
    item_id = World.create_entity(position, renderable, name, item, equippable, defense_bonus)
    return item_id
