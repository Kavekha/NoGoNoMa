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
from components.equippable_component import EquippableComponent
from components.bonus_components import PowerBonusComponent, DefenseBonusComponent
from data.items_enum import EquipmentSlots
from world import World
from ui_system.ui_enums import Layers


RAW_PATH = "/raws"


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
        self.weapon = {'range': None,
                       'power_bonus': None}
        self.shield = {'defense_bonus': None}


class RawsMob:
    def __init__(self):
        self.name = None
        self.renderable = None
        self.blocks_tile = True
        self.stats = {
            'max_hp': 1,
            'hp': 1,
            'defense': 0,
            'power': 0
        }
        self.vision_range = 5


class RawsMaster:
    items = []
    mobs = []
    item_index = {}
    mob_index = {}

    @staticmethod
    def load_index():
        for i, item in enumerate(RawsMaster.items):
            RawsMaster.item_index[item.name] = i + 1

        for i, mob in enumerate(RawsMaster.mobs):
            RawsMaster.mob_index[mob.name] = i + 1

    @staticmethod
    def load_raws():
        full_path = os.getcwd() + RAW_PATH
        full_path = '../raws'

        print(f'current working dir is {os.getcwd()}')
        print(f'path should be {os.getcwd() + RAW_PATH}')
        print(f'full path is {full_path}')
        for file in os.listdir(full_path):
            RawsMaster.load_raw(file)

        RawsMaster.load_index()
        print(f'---- raws loaded -------')

    @staticmethod
    def load_raw(file):
        print(f'I have receive {file}')
        full_path = os.getcwd() + RAW_PATH + '/' + file
        full_path = '../raws/' + file
        with open(full_path, 'r') as json_file:
            datas = json.load(json_file)
            for data in datas:
                if data == "items":
                    RawsMaster.load_item_raw(datas[data])
                elif data == 'mobs':
                    RawsMaster.load_mob_raw(datas[data])
                else:
                    print(f'load raw: Data was not items but {data}')
                    raise NotImplementedError

    @staticmethod
    def load_mob_raw(data):
        for mob in data:
            raw_mob = RawsMob()
            for component in mob:
                if component == 'name':
                    raw_mob.name = mob[component]
                elif component == 'renderable':
                    raw_mob.renderable = RawsMaster.load_renderable_raw(mob[component])
                elif component == 'blocks_tile':
                    raw_mob.blocks_tile = mob[component]
                elif component == 'stats':
                    raw_mob.stats = RawsMaster.load_stats_raw(mob[component])
                elif component == 'vision_range':
                    raw_mob.vision_range = int(mob[component])
                else:
                    print(f'Unknown component {component} for mob {mob}')
                    raise NotImplementedError
            RawsMaster.mobs.append(raw_mob)

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
                elif component == 'weapon':
                    raw_item.weapon = RawsMaster.load_weapon_raw(item[component])
                elif component == 'shield':
                    raw_item.shield = RawsMaster.load_shield_raw(item[component])
                else:
                    print(f'load item raw: unkown component in {component}')
                    raise NotImplementedError
            RawsMaster.items.append(raw_item)

    @staticmethod
    def load_shield_raw(shield_component):
        shield_attributes = {}
        for attribute in shield_component:
            if attribute == 'defense_bonus':
                shield_attributes['defense_bonus'] = int(shield_component[attribute])
            else:
                print(f'Missing attribute for shield in {shield_component}')
                raise NotImplementedError

    @staticmethod
    def load_weapon_raw(weapon):
        weap = {}
        for attribute in weapon:
            if attribute == 'range':
                weap['range'] = weapon[attribute]
            elif attribute == 'power_bonus':
                weap['power_bonus'] = int(weapon[attribute])
            else:
                print(f'Missing attribute for weapon in {weap}')
                raise NotImplementedError

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
                print(f'load render raw: unknown attribute {attribute} in {renderable}')
                raise NotImplementedError
        return render

    @staticmethod
    def load_stats_raw(stats_component):
        stats = {}
        for attribute in stats_component:
            if attribute == 'max_hp':
                stats['max_hp'] = int(stats_component[attribute])
            elif attribute == 'hp':
                stats['_hp'] = int(stats_component[attribute])
            elif attribute == 'defense':
                stats['defense'] = int(stats_component[attribute])
            elif attribute == 'power':
                stats['power'] = int(stats_component[attribute])
            else:
                print(f'load stat raws: unknown attribute {attribute} in {stats_component}')
        return stats

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
    def create_something(name, x, y):
        print(f'------ spawn something')
        print(f'create: name is {name}')
        if RawsMaster.item_index.get(name):
            return RawsMaster.create_item(name, x, y)
        if RawsMaster.mob_index.get(name):
            return RawsMaster.create_mob(name, x, y)
        return

    @staticmethod
    def create_mob(name, x, y):
        to_create = RawsMaster.mobs[RawsMaster.mob_index[name] - 1]

        components_for_entity = []

        components_for_entity.append(PositionComponent(x, y))
        components_for_entity.append(ItemComponent())

        if to_create.name:
            components_for_entity.append(NameComponent(to_create.name))

        if to_create.renderable:
            components_for_entity.append(RenderableComponent(to_create.renderable['glyph'],
                                                             to_create.renderable['fg'],
                                                             to_create.renderable['order']))

        from components.blocktile_component import BlockTileComponent
        from components.combat_stats_component import CombatStatsComponent
        from components.viewshed_component import ViewshedComponent

        if to_create.blocks_tile:
            components_for_entity.append(BlockTileComponent)

        if to_create.stats:
            if to_create.stats.get('max_hp') and to_create.stats.get('power') and to_create.stats.get('defense'):
                components_for_entity.append(CombatStatsComponent(to_create.stats.get('max_hp'),
                                                                  to_create.stats.get('defense'),
                                                                  to_create.stats.get('power')
                                                                  )
                                             )
        if to_create.vision_range:
            components_for_entity.append(ViewshedComponent(to_create.vision_range))

        World.create_entity([components_for_entity])
        return True

    @staticmethod
    def create_item(name, x, y):
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

        if to_create.weapon:
            components_for_entity.append(EquippableComponent(EquipmentSlots.MELEE))

            if to_create.weapon.get('power_bonus'):
                components_for_entity.append(PowerBonusComponent(to_create['weapon']['power_bonus']))

        if to_create.shield:
            components_for_entity.append(EquippableComponent(EquipmentSlots.SHIELD))

            if to_create.shield.get('defense_bonus'):
                components_for_entity.append(DefenseBonusComponent(to_create['shield']['defense_bonus']))

        World.create_entity([components_for_entity])
        return True


if __name__ == "__main__":
    x = 0
    y = 0
    RawsMaster()
    RawsMaster.load_raws()

    to_test = ['HEALTH_POTION', 'CONFUSION_SCROLL', 'FIREBALL_SCROLL', 'MISSILE_MAGIC_SCROLL',
               'DAGGER', "LONGSWORD", "BUCKLET", "TOWER_SHIELD", "MORBLIN", "OOGLOTH"]
    for item in to_test:
        RawsMaster.create_something(item, x, y)
        print(f'---------------')

    print(f'world component is {World.get_all_entities()}')
    print(f'self item index is {RawsMaster.item_index}')
    print(f'self mob index is {RawsMaster.mob_index}')
