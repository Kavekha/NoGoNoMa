import json
import os

from components.position_component import PositionComponent
from components.name_component import NameComponent
from components.renderable_component import RenderableComponent
from components.consumable_component import ConsumableComponent
from components.provides_healing_component import ProvidesHealingComponent
from components.inflicts_damage_component import InflictsDamageComponent
from components.ranged_component import RangedComponent
from components.area_effect_component import AreaOfEffectComponent
from components.confusion_component import ConfusionComponent
from components.item_component import ItemComponent
from world import World
from ui_system.ui_enums import Layers


RAW_PATH = "/raws/"


class RawsItem:
    def __init__(self):
        self.name = None
        self.renderable = None
        self.consumable = None


class RawsRenderable:
    def __init__(self):
        self.glyph = None
        self.fg = None
        self.order = None


class RawsConsumable:
    def __init__(self):
        self.effects = None


class RawsEffect:
    def __init__(self):
        self.provides_healing = None
        self.damage = None
        self.ranged = None
        self.area_of_effect = None
        self.confusion = None


class RawsMaster:
    items = []
    item_index = {}

    @staticmethod
    def load_index():
        for i, item in enumerate(RawsMaster.items):
            RawsMaster.item_index[item.name] = i + 1

    @staticmethod
    def load_raws():
        print(f'current working dir is {os.getcwd()}')
        print(f'path should be {os.getcwd() + RAW_PATH}')
        for file in os.listdir(os.getcwd() + RAW_PATH):
            RawsMaster.load_raw(file)

        RawsMaster.load_index()
        print(f'---- raws loaded -------')

    @staticmethod
    def load_raw(file):
        print(f'I have receive {file}')
        with open(os.getcwd() + RAW_PATH + file, 'r') as json_file:
            datas = json.load(json_file)
            for data in datas:
                if data == "items":
                    RawsMaster.load_item_raw(datas[data])
                else:
                    print(f'load raw: Data was not items but {data}')
                    raise NotImplementedError

    @staticmethod
    def load_renderable_raw(renderable):
        render = RawsRenderable()
        for attribute in renderable:
            # print(f'attribute for render is {attribute}')
            if attribute == "glyph":
                # print(f'attribute glyph is {item[component][attribute]}')
                render.glyph = renderable[attribute]
            elif attribute == "fg":
                render.fg = renderable[attribute]
            elif attribute == "order":
                render.order = Layers(renderable[attribute])
            else:
                print(f'load render raw: unkown attribute in {renderable}')
                raise NotImplementedError
        return render

    @staticmethod
    def load_consumable_raw(consumable):
        consum = RawsConsumable()
        for attribute in consumable:
            if attribute == 'effects':
                raw_effects = RawsEffect()
                for effect in consumable[attribute]:
                    if effect == "provides_healing":
                        raw_effects.provides_healing = int(consumable[attribute][effect])
                    elif effect == "damage":
                        raw_effects.damage = int(consumable[attribute][effect])
                    elif effect == "ranged":
                        raw_effects.ranged = int(consumable[attribute][effect])
                    elif effect == "area_of_effect":
                        raw_effects.area_of_effect = int(consumable[attribute][effect])
                    elif effect == "confusion":
                        raw_effects.confusion = int(consumable[attribute][effect])
                    else:
                        print(f'load consum raw: unknown effect in {consumable[attribute]}')
                        raise NotImplementedError
                consum.effects = raw_effects
            else:
                print(f'load consumable raw: unkown attribute in {consumable}')
                raise NotImplementedError
        return consum

    @staticmethod
    def load_item_raw(data):
        for item in data:
            raw_item = RawsItem()
            for component in item:
                if component == 'name':
                    raw_item.name = item[component]
                elif component == 'renderable':
                    raw_item.renderable = RawsMaster.load_renderable_raw(item[component])
                elif component == 'consumable':
                    raw_item.consumable = RawsMaster.load_consumable_raw(item[component])
                else:
                    print(f'load item raw: unkown component in {component}')
                    raise NotImplementedError
            RawsMaster.items.append(raw_item)

    @staticmethod
    def create_item(name, x, y):
        print(f'create: name is {name}')
        print(f'self item index is {RawsMaster.item_index}')
        if not RawsMaster.item_index.get(name):
            return

        to_create = RawsMaster.items[RawsMaster.item_index[name] - 1]
        pos = PositionComponent(x, y)
        id = World.create_entity(pos)
        print(f'TO CREATE : id {id}, name {name}')

        item = ItemComponent()
        World.add_component(item, id)

        if to_create.name:
            name = NameComponent(to_create.name)
            World.add_component(name, id)

        if to_create.renderable:
            render = RenderableComponent(to_create.renderable.glyph, to_create.renderable.fg, to_create.renderable.order)
            World.add_component(render, id)

        if to_create.consumable:
            consum = ConsumableComponent()
            World.add_component(consum, id)

        if to_create.consumable.effects:
            if to_create.consumable.effects.provides_healing:
                provide_heal = ProvidesHealingComponent(to_create.consumable.effects.provides_healing)
                print(f'provide heal is {provide_heal.healing_amount}')
                World.add_component(provide_heal, id)

            if to_create.consumable.effects.damage:
                inflict_dmg = InflictsDamageComponent(to_create.consumable.effects.damage)
                World.add_component(inflict_dmg, id)

            if to_create.consumable.effects.ranged:
                ranged = RangedComponent(to_create.consumable.effects.ranged)
                World.add_component(ranged, id)

            if to_create.consumable.effects.area_of_effect:
                print(f'aoe: {to_create.consumable.effects.area_of_effect}')
                area = AreaOfEffectComponent(to_create.consumable.effects.area_of_effect)
                World.add_component(area, id)

            if to_create.consumable.effects.confusion:
                confusion = ConfusionComponent(to_create.consumable.effects.confusion)
                World.add_component(confusion, id)
        return True


if __name__ == "__main__":
    x = 0
    y = 0
    RawsMaster()
    RawsMaster.load_raws()

    to_test = ['HEALTH_POTION', 'CONFUSION_SCROLL', 'FIREBALL_SCROLL', 'MISSILE_MAGIC_SCROLL']
    for item in to_test:
        RawsMaster.create_item(item, x, y)

    print(f'world component is {World.get_all_entities()}')

