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


RAW_PATH = "../raws"


class RawsItem:
    def __init__(self):
        self.name = None
        self.renderable = {'glyph': None, 'fg': None, 'order': None}
        self.consumable = {'effects': {
            'provides_healing': None,
        'damage': None,
        'ranged': None,
        'area_of_effect': None,
        'confusion': None}
        }



class RawsMaster:
    items = []
    item_index = {}

    @staticmethod
    def load_index():
        for i, item in enumerate(RawsMaster.items):
            RawsMaster.item_index[item.name] = i + 1

    @staticmethod
    def load_raws():
        full_path = os.path.join(os.getcwd(), RAW_PATH)

        print(f'current working dir is {os.getcwd()}')
        print(f'path should be {os.getcwd() + RAW_PATH}')
        for file in os.listdir(full_path):
            RawsMaster.load_raw(file)

        RawsMaster.load_index()
        print(f'---- raws loaded -------')

    @staticmethod
    def load_raw(file):
        print(f'I have receive {file}')
        full_path = os.path.join(os.getcwd(), RAW_PATH, file)
        with open(full_path, 'r') as json_file:
            datas = json.load(json_file)
            for data in datas:
                if data == "items":
                    RawsMaster.load_item_raw(datas[data])
                else:
                    print(f'load raw: Data was not items but {data}')
                    raise NotImplementedError

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
    def load_renderable_raw(renderable):
        render = {}
        for attribute in renderable:
            # print(f'attribute for render is {attribute}')
            if attribute == "glyph":
                # print(f'attribute glyph is {item[component][attribute]}')
                render['glyph'] = renderable[attribute]
            elif attribute == "fg":
                render['fg'] = renderable[attribute]
            elif attribute == "order":
                render['order'] = Layers(renderable[attribute])
            else:
                print(f'load render raw: unknown attribute in {renderable}')
                raise NotImplementedError
        return render

    @staticmethod
    def load_consumable_raw(consumable):
        for attribute in consumable:
            raw_consumable = {}
            if attribute == 'effects':
                raw_effects = {}
                for effect in consumable[attribute]:
                    if effect == "provides_healing":
                        raw_effects["provides_healing"] = int(consumable[attribute][effect])
                    elif effect == "damage":
                        raw_effects["damage"] = int(consumable[attribute][effect])
                    elif effect == "ranged":
                        raw_effects["ranged"] = int(consumable[attribute][effect])
                    elif effect == "area_of_effect":
                        raw_effects["area_of_effect"] = int(consumable[attribute][effect])
                    elif effect == "confusion":
                        raw_effects["confusion"] = int(consumable[attribute][effect])
                    else:
                        print(f'load consum raw: unknown effect in {consumable[attribute]}')
                        raise NotImplementedError
                raw_consumable['effects'] = raw_effects
            else:
                print(f'load consumable raw: unkown attribute in {consumable}')
                raise NotImplementedError
            return raw_consumable

    @staticmethod
    def create_item(name, x, y):
        print(f'create: name is {name}')
        print(f'self item index is {RawsMaster.item_index}')
        if not RawsMaster.item_index.get(name):
            return

        to_create = RawsMaster.items[RawsMaster.item_index[name] - 1]
        print(f'item raw contains: {to_create.name}\n {to_create.renderable}\n {to_create.consumable}')

        components_for_entity = []

        components_for_entity.append(PositionComponent(x, y))
        components_for_entity.append(ItemComponent())

        if to_create.name:
            components_for_entity.append(NameComponent(to_create.name))

        if to_create.renderable:
            components_for_entity.append(RenderableComponent(to_create.renderable['glyph'],
                                                             to_create.renderable['fg'],
                                                             to_create.renderable['order']))

        if to_create.consumable:
            components_for_entity.append(ConsumableComponent())

        if to_create.consumable.get('effects'):
            if to_create.consumable['effects'].get('provides_healing'):
                components_for_entity.append(ProvidesHealingComponent(
                    to_create.consumable['effects']['provides_healing']))

            if to_create.consumable['effects'].get('damage'):
                components_for_entity.append(InflictsDamageComponent(to_create.consumable['effects']['damage']))

            if to_create.consumable['effects'].get('ranged'):
                components_for_entity.append(RangedComponent(to_create.consumable['effects']['ranged']))

            if to_create.consumable['effects'].get('area_of_effect'):
                components_for_entity.append(AreaOfEffectComponent(to_create.consumable['effects']['area_of_effect']))

            if to_create.consumable['effects'].get('confusion'):
                components_for_entity.append(ConfusionComponent(to_create.consumable['effects']['confusion']))

        World.create_entity([components_for_entity])
        return True


if __name__ == "__main__":
    x = 0
    y = 0
    RawsMaster()
    RawsMaster.load_raws()

    to_test = ['HEALTH_POTION', 'CONFUSION_SCROLL', 'FIREBALL_SCROLL', 'MISSILE_MAGIC_SCROLL']
    for item in to_test:
        RawsMaster.create_item(item, x, y)
        print(f'---------------')

    print(f'world component is {World.get_all_entities()}')

