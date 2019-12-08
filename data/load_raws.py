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
from components.monster_component import MonsterComponent
from components.blocktile_component import BlockTileComponent
from components.combat_stats_component import CombatStatsComponent
from components.viewshed_component import ViewshedComponent
from components.attributes_component import AttributesComponent
from components.skills_component import Skills, SkillsComponent
from components.pools_component import Pools

from systems.game_system import npc_hp_at_lvl, mana_point_at_level
from data.items_enum import EquipmentSlots
from data.raws_structs import RawsItem, RawsMob, RawsSpawnTable
from world import World
from ui_system.ui_enums import Layers
import config


class RawsMaster:
    items = []
    mobs = []
    spawn_table = []
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
        print(f'------- load raws ------')
        full_path = os.getcwd() + config.RAW_FILES  # game
        # full_path = '../raws'

        for file in os.listdir(full_path):
            RawsMaster.load_raw(file)

        RawsMaster.load_index()
        print(f'---- raws loaded -------')

        print(f'item index is {RawsMaster.item_index}')
        print(f'mob index is {RawsMaster.mob_index}')

    @staticmethod
    def load_raw(file):
        # full_path = '../raws/' + file   # load raws
        full_path = os.getcwd() + config.RAW_FILES + '/' + file # game
        with open(full_path, 'r') as json_file:
            print(f'--- loading raw {file} ----')
            datas = json.load(json_file)
            for data in datas:
                # print(f'data is {data}')
                if data == "items":
                    RawsMaster.load_item_raw(datas[data])
                elif data == 'mobs':
                    RawsMaster.load_mob_raw(datas[data])
                elif data == 'spawn_table':
                    RawsMaster.load_spawn_table_raw(datas[data])
                else:
                    print(f'load raw: Data was not items but {data}')
                    raise NotImplementedError

    @staticmethod
    def load_spawn_table_raw(data):
        print(f'--- load spawn tables ---')
        raw_table = RawsSpawnTable()
        for spawn_entry in data:
            object_entry = {}
            name = None
            for info in spawn_entry:
                print(f'current info is {info}')
                if info == 'name' and not object_entry:
                    name = spawn_entry[info]
                    print(f'table: name : {info}, object entry is {object_entry} and name is {name}')
                elif info == 'weight' and name:
                    object_entry[info] = int(spawn_entry[info])
                    print(f'table: weight: table object entry is now {object_entry}')
                elif info == 'min_depth' and name:
                    object_entry[info] = int(spawn_entry[info])
                elif info == 'max_depth' and name:
                    object_entry[info] = int(spawn_entry[info])
                elif info == 'add_map_depth_to_weight'and name:
                    object_entry[info] = spawn_entry[info]
                else:
                    print(f'spawn table raw: info is {info} and spawn entry is {spawn_entry}')
                    raise NotImplementedError
            if object_entry:
                raw_table.spawn_infos[name] = object_entry
        print(f'load table: raw table is {raw_table}')
        print(f'load table: raw table content is {raw_table.spawn_infos}')
        RawsMaster.spawn_table.append(raw_table)

    @staticmethod
    def get_spawn_table_for_depth(depth):
        from data.random_table import RandomTable
        table_depth = RandomTable()
        for table in RawsMaster.spawn_table:
            available_spawns = []
            for entry in table.spawn_infos:
                print(f'get depth: entry is {entry}')
                mind, maxd = table.spawn_infos[entry].get('min_depth', 0), table.spawn_infos[entry].get('max_depth', 0)
                if mind <= depth and maxd >= depth:
                    print(f'get depth: {entry} is available at this depth level')
                    available_spawns.append((entry, table.spawn_infos[entry].get('weight', 0)))

            if available_spawns:
                for spawn, weight in available_spawns:
                    table_depth.add(spawn, weight)

        print(f'table_depth is:')
        for entry in table_depth.entries:
            print(f'- {entry.name}, {entry.weight}')

        return table_depth


    @staticmethod
    def load_mob_raw(data):
        print(f'---- load mob ---')
        for mob in data:
            raw_mob = RawsMob()
            for component in mob:
                if component == 'name':
                    raw_mob.name = mob[component]
                elif component == 'renderable':
                    raw_mob.renderable = RawsMaster.load_renderable_raw(mob[component])
                elif component == 'blocks_tile':
                    raw_mob.blocks_tile = mob[component]
                elif component == 'vision_range':
                    raw_mob.vision_range = int(mob[component])
                elif component == 'attributes':
                    raw_mob.attributes = RawsMaster.load_attributes_raw(mob[component])
                elif component == 'skills':
                    raw_mob.skills = RawsMaster.load_skills_raw(mob[component])
                elif component == 'level':
                    raw_mob.lvl = mob[component]
                else:
                    print(f'Unknown component {component} for mob {mob}')
                    raise NotImplementedError
            RawsMaster.mobs.append(raw_mob)

    @staticmethod
    def load_item_raw(data):
        print(f'---- load item ---')
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
        return shield_attributes

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
        return weap

    @staticmethod
    def load_attributes_raw(attributes_raw):
        attributes = {}
        for attribute in attributes_raw:
            if attribute == 'might' or attribute == 'body' or attribute == 'wits' or attribute == 'quickness':
                attributes[attribute] = attributes_raw[attribute]
        return attributes

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
    def load_skills_raw(skills_component):
        skills = {}
        for skill in skills_component:
            # valid skill?
            if skill == 'melee':
                real_skill = Skills.MELEE
            else:
                print(f'load skills raw: Unknown skill {skill}')
                raise NotImplementedError
            skills[real_skill] = skills_component[skill]
        return skills

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
    def spawn_named_entity(name, x, y):
        print(f'------ spawn something')
        print(f'spawn name entity: '
              f'name requested was {name},'
              f' \n index item is {RawsMaster.item_index} \n index mob is {RawsMaster.mob_index}')
        if RawsMaster.item_index.get(name):
            print(f'item name found')
            return RawsMaster.create_item(name, x, y)
        if RawsMaster.mob_index.get(name):
            print('monster found')
            return RawsMaster.create_mob(name, x, y)
        return

    @staticmethod
    def create_mob(name, x, y):
        to_create = RawsMaster.mobs[RawsMaster.mob_index[name] - 1]
        components_for_entity = [MonsterComponent()]

        if to_create.name:
            components_for_entity.append(NameComponent(to_create.name))

        if to_create.renderable:
            components_for_entity.append(RenderableComponent(to_create.renderable['glyph'],
                                                             to_create.renderable['fg'],
                                                             to_create.renderable['order']))

        if to_create.blocks_tile:
            components_for_entity.append(BlockTileComponent)

        if to_create.vision_range:
            components_for_entity.append(ViewshedComponent(to_create.vision_range))

        if to_create.attributes:
            components_for_entity.append(AttributesComponent(might=to_create.attributes.get('might', 1),
                                                             body=to_create.attributes.get('body', 1),
                                                             quickness=to_create.attributes.get('quickness', 1),
                                                             wits=to_create.attributes.get('wits', 1)
                                                             ))

        if to_create.skills:
            skill_component = SkillsComponent()
            for skill in to_create.skills:
                skill_component.skills[skill] = to_create.skills[skill]
            components_for_entity.append(SkillsComponent())

        if to_create.lvl:
            mob_lvl = to_create.lvl
        else:
            mob_lvl = 1
        mob_hp = npc_hp_at_lvl(to_create.attributes.get('body', config.DEFAULT_MONSTER_BODY_ATTRIBUTE), mob_lvl)
        mob_mana = mana_point_at_level(to_create.attributes.get('wits', config.DEFAULT_MONSTER_WITS_ATTRIBUTE), mob_lvl)
        print(f'create mob: pools: {mob_lvl}, hp {mob_hp}, mana {mob_mana}')

        components_for_entity.append(Pools(mob_hp, mob_mana, mob_lvl))

        mob_id = World.create_entity(PositionComponent(x, y))
        print(f'components in components for entity is {components_for_entity}')
        for component in components_for_entity:
            World.add_component(component, mob_id)

        return True

    @staticmethod
    def create_item(name, x, y):
        to_create = RawsMaster.items[RawsMaster.item_index[name] - 1]
        # print(f'item raw contains: {to_create.name}\n {to_create.renderable}\n {to_create.consumable}')

        components_for_entity = [ItemComponent()]

        if to_create.name:
            components_for_entity.append(NameComponent(to_create.name))
            print(f'item {name} has component Name {to_create.name}')

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
            print(f'to create is {to_create} and Equippable Melee component has been requested')
            components_for_entity.append(EquippableComponent(EquipmentSlots.MELEE))

            if to_create.weapon.get('power_bonus'):
                components_for_entity.append(PowerBonusComponent(to_create.weapon['power_bonus']))

        if to_create.shield:
            print(f'to create is {to_create} and Equippable Shield component has been requested')
            components_for_entity.append(EquippableComponent(EquipmentSlots.SHIELD))

            if to_create.shield.get('defense_bonus'):
                components_for_entity.append(DefenseBonusComponent(to_create.shield['defense_bonus']))

        item_id = World.create_entity(PositionComponent(x, y))
        for component in components_for_entity:
            World.add_component(component, item_id)

        print(f'check item creation : {item_id}, name component {World.get_entity_component(item_id, NameComponent)}')
        print(f'check item creation Name : {World.get_entity_component(item_id, NameComponent)}')

        return True


if __name__ == "__main__":
    x = 0
    y = 0
    RawsMaster()
    RawsMaster.load_raws()

    to_test = ['HEALTH_POTION', 'CONFUSION_SCROLL', 'FIREBALL_SCROLL', 'MISSILE_MAGIC_SCROLL',
               'DAGGER', "LONGSWORD", "BUCKLET", "TOWER_SHIELD", "MORBLIN", "OOGLOTH"]
    for item in to_test:
        RawsMaster.spawn_named_entity(item, x, y)
        print(f'---------------')

    print(f'world component is {World.get_all_entities()}')
    print(f'self item index is {RawsMaster.item_index}')
    print(f'self mob index is {RawsMaster.mob_index}')

    print(f'------ spawn table -----')
    RawsMaster.get_spawn_table_for_depth(1)
