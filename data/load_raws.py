import json
import os

from components.position_component import PositionComponent
from components.name_component import NameComponent
from components.renderable_component import RenderableComponent
from components.consumable_component import ConsumableComponent
from components.provides_healing_component import ProvidesHealingComponent
from components.inflicts_damage_component import InflictsDamageComponent
from components.ranged_component import RangedComponent
from world import World


RAW_PATH = "../raws/"


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


class Raws:
    def __init__(self):
        self.items = []
        self.item_index = {}

    def load_index(self):
        for i, item in enumerate(self.items):
            self.item_index[item.name] = i + 1

    def load_raws(self):
        from os.path import isfile, join
        json_files = [f for f in os.listdir(RAW_PATH) if isfile(join(RAW_PATH, f)) and f.endswith(".json")]

        for file in json_files:
            self.load_raw(file)

        self.load_index()

    def load_raw(self, file):
        with open(file, 'r') as json_file:
            datas = json.load(json_file)
            for data in datas:
                if data == "items":
                    self.load_item_raw(datas[data])

    def load_renderable_raw(self, renderable):
        render = RawsRenderable()
        for attribute in renderable:
            # print(f'attribute for render is {attribute}')
            if attribute == "glyph":
                # print(f'attribute glyph is {item[component][attribute]}')
                render.glyph = renderable[attribute]
            elif attribute == "fg":
                render.fg = renderable[attribute]
            elif attribute == "order":
                render.order = renderable[attribute]
        return render

    def load_consumable_raw(self, consumable):
        consum = RawsConsumable()
        for attribute in consumable:
            if attribute == 'effects':
                raw_effects = RawsEffect()
                for effect in consumable[attribute]:
                    if effect == "provides_healing":
                        raw_effects.provides_healing = consumable[attribute][effect]
                    elif effect == "damage":
                        raw_effects.damage = consumable[attribute][effect]
                    elif effect == "ranged":
                        raw_effects.ranged = consumable[attribute][effect]
                    else:
                        raise NotImplementedError
                consum.effects = raw_effects
        return consum

    def load_item_raw(self, data):
        for item in data:
            raw_item = RawsItem()
            for component in item:
                if component == 'name':
                    raw_item.name = item[component]
                elif component == 'renderable':
                    raw_item.renderable = self.load_renderable_raw(item[component])
                elif component == 'consumable':
                    raw_item.consumable = self.load_consumable_raw(item[component])
                else:
                    raise NotImplementedError
            self.items.append(raw_item)

    def create_item(self, name, x, y):
        if not self.item_index.get(name):
            raise KeyError

        to_create = self.items[self.item_index[name]]
        pos = PositionComponent(x, y)
        id = World.create_entity(pos)

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
                World.add_component(provide_heal, id)

            if to_create.consumable.effects.damage:
                inflict_dmg = InflictsDamageComponent(to_create.consumable.effects.damage)
                World.add_component(inflict_dmg, id)

            if to_create.consumable.effects.ranged:
                ranged = RangedComponent(to_create.consumable.effects.ranged)
                World.add_component(ranged, id)


if __name__ == "__main__":
    x = 0
    y = 0
    raws = Raws()
    raws.load_raws()

    raws.create_item('HEALTH_POTION', x, y)

    print(f'world component is {World.get_all_entities()}')

