import json
import os

from components.position_components import PositionComponent
from components.name_components import NameComponent, ObfuscatedNameComponent
from components.renderable_component import RenderableComponent
from components.provide_effects_components import ProvidesHealingComponent, ProvidesCurseRemovalComponent, \
    ProvidesIdentificationComponent
from components.inflicts_damage_component import InflictsDamageComponent
from components.ranged_component import RangedComponent
from components.area_effect_component import AreaOfEffectComponent
from components.status_effect_components import ConfusionComponent, DurationComponent
from components.item_components import ItemComponent, MeleeWeaponComponent, WearableComponent, ConsumableComponent
from components.equip_components import EquippableComponent
from components.blocktile_component import BlockTileComponent, BlockVisibilityComponent
from components.viewshed_component import ViewshedComponent
from components.character_components import AttributesComponent, MonsterComponent, AttributeBonusComponent
from components.skills_component import Skills, SkillsComponent
from components.pools_component import Pools
from components.natural_attack_defense_component import NaturalAttackDefenseComponent, NaturalAttack
from components.magic_item_components import MagicItemComponent, CursedItemComponent
from components.hidden_component import HiddenComponent
from components.triggers_components import EntryTriggerComponent, ActivationComponent
from components.door_component import DoorComponent
from components.initiative_components import InitiativeComponent
from components.particule_components import SpawnParticuleBurstComponent, SpawnParticuleLineComponent

from player_systems.game_system import npc_hp_at_lvl, mana_point_at_level
from data.components_enum import EquipmentSlots, WeaponAttributes, MagicItemClass
from data.raws_structs import RawsItem, RawsMob, RawsSpawnTable
from data.load_raws import parse_particule
from world import World
from ui_system.ui_enums import Layers
import config


class RawsMaster:
    items = []
    mobs = []
    spawn_table = []
    natural_attacks = []
    props = []
    item_index = {}
    mob_index = {}
    natural_attacks_index = {}
    props_index = {}

    @staticmethod
    def load_index():
        for i, item in enumerate(RawsMaster.items):
            RawsMaster.item_index[item.name] = i + 1

        for i, mob in enumerate(RawsMaster.mobs):
            RawsMaster.mob_index[mob.name] = i + 1

        for i, attack in enumerate(RawsMaster.natural_attacks):
            RawsMaster.natural_attacks_index[attack["name"]] = i + 1

        for i, prop in enumerate(RawsMaster.props):
            RawsMaster.props_index[prop["name"]] = i + 1

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
        full_path = os.getcwd() + config.RAW_FILES + '/' + file  # game
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
                elif data == 'natural_attacks':
                    RawsMaster.load_natural_attacks_raw(datas[data])
                elif data == 'props':
                    RawsMaster.load_props_raw(datas[data])
                else:
                    print(f'load raw: Data type {data} not supported')
                    raise NotImplementedError

    @staticmethod
    def load_props_raw(data):
        for prop_raw in data:
            props = {}
            for component in prop_raw:
                if component == 'name':
                    props[component] = prop_raw[component]
                elif component == 'renderable':
                    props[component] = RawsMaster.load_renderable_raw(prop_raw[component])
                elif component == 'hidden':
                    props[component] = prop_raw[component]
                elif component == 'entry_trigger':
                    props[component] = prop_raw[component]
                elif component == 'blocks_tile':
                    props[component] = prop_raw[component]
                elif component == 'blocks_visibility':
                    props[component] = prop_raw[component]
                elif component == 'door_open':
                    props[component] = prop_raw[component]
                else:
                    print(f'prop component {component} is not implemented for props')
                    raise NotImplementedError
            print(f'PROP : prop created with {props}')
            RawsMaster.props.append(props)

    @staticmethod
    def load_natural_attacks_raw(data):
        for attack in data:
            natural_attack = {}
            for component in attack:
                if component == 'name':
                    natural_attack[component] = attack[component]
                elif component == 'attribute':
                    if attack[component] == 'might':
                        natural_attack[component] = WeaponAttributes.MIGHT
                    elif attack[component] == 'quickness':
                        natural_attack[component] = WeaponAttributes.QUICKNESS
                    else:
                        print(f'natural attack attribute {attack[component]} not implemented')
                        raise NotImplementedError
                elif component == 'hit_bonus':
                    natural_attack[component] = int(attack[component])
                elif component == 'min_dmg':
                    natural_attack[component] = int(attack[component])
                elif component == 'max_dmg':
                    natural_attack[component] = int(attack[component])
                elif component == 'dmg_bonus':
                    natural_attack[component] = int(attack[component])
                else:
                    print(f'component {component} in attack {attack} not implemented')
                    raise NotImplementedError
            RawsMaster.natural_attacks.append(natural_attack)

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
                elif info == 'add_map_depth_to_weight' and name:
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
                elif component == 'natural':
                    raw_mob.natural = RawsMaster.load_natural_def_attack_raw(mob[component])
                else:
                    print(f'Unknown component {component} for mob {mob}')
                    raise NotImplementedError
            RawsMaster.mobs.append(raw_mob)

    @staticmethod
    def load_natural_def_attack_raw(data):
        naturals = {}
        for natural in data:
            if natural == 'armor':
                naturals[natural] = data[natural]
            elif natural == 'attacks':
                naturals[natural] = RawsMaster.load_mob_natural_attacks_raw(data[natural])
            else:
                print(f'load natural {natural} not implemented')
                raise NotImplementedError
        return naturals

    @staticmethod
    def load_mob_natural_attacks_raw(natural_attacks_raw):
        natural_attacks = list()
        for attack in natural_attacks_raw:
            natural_attacks.append(attack)
        return natural_attacks

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
                elif component == 'wearable':
                    raw_item.wearable = RawsMaster.load_wearable_raw(item[component])
                elif component == 'magic':
                    raw_item.magic = RawsMaster.load_magic_item_raw(item[component])
                elif component == 'attributes':
                    raw_item.attributes = RawsMaster.load_attributes_bonus_raw(item[component])
                else:
                    print(f'load item raw: unkown component in {component}')
                    raise NotImplementedError
            RawsMaster.items.append(raw_item)

    @staticmethod
    def load_attributes_bonus_raw(attributes_component):
        bonus_attributes = dict()
        for bonus in attributes_component:
            if bonus == 'might':
                bonus_attributes[bonus] = int(attributes_component.get(bonus))
            elif bonus == 'body':
                bonus_attributes[bonus] = int(attributes_component.get(bonus))
            elif bonus == 'quickness':
                bonus_attributes[bonus] = int(attributes_component.get(bonus))
            elif bonus == 'wits':
                bonus_attributes[bonus] = int(attributes_component.get(bonus))
            else:
                print(f'Attribute bonus {bonus} not implemented in load attributes bonus')
                raise NotImplementedError
        return bonus_attributes

    @staticmethod
    def load_magic_item_raw(magic_component):
        magic_attributes = dict()
        for attribute in magic_component:
            if attribute == 'class':
                if magic_component[attribute] == 'common':
                    magic_attributes[attribute] = MagicItemClass.COMMON
                elif magic_component[attribute] == 'uncommon':
                    magic_attributes[attribute] = MagicItemClass.UNCOMMON
                else:
                    print(f'magic class {magic_component[attribute]} not implemented in magic item raw')
                    raise NotImplementedError
            elif attribute == 'naming':
                if magic_component[attribute] == 'scroll':
                    magic_attributes[attribute] = magic_component[attribute]
                elif magic_component[attribute] == 'potion':
                    magic_attributes[attribute] = magic_component[attribute]
                else:
                    magic_attributes[attribute] = magic_component[attribute]
                    print(
                        f'WARNING: In magic naming, attribute {magic_component[attribute]} not implemented for component {magic_component}')
            elif attribute == 'cursed':
                magic_attributes[attribute] = magic_component[attribute]
            else:
                print(f'magic attribute {attribute} not implemented in magic item raw')
                raise NotImplementedError
        return magic_attributes

    @staticmethod
    def load_wearable_raw(wearable_component):
        wearable_attributes = dict()
        for attribute in wearable_component:
            if attribute == 'armor':
                wearable_attributes[attribute] = int(wearable_component[attribute])
            elif attribute == 'slot':
                if wearable_component[attribute] == 'shield':
                    wearable_attributes[attribute] = EquipmentSlots.SHIELD
                elif wearable_component[attribute] == 'torso':
                    wearable_attributes[attribute] = EquipmentSlots.TORSO
                elif wearable_component[attribute] == 'helm':
                    wearable_attributes[attribute] = EquipmentSlots.HELM
                elif wearable_component[attribute] == 'gauntlet':
                    wearable_attributes[attribute] = EquipmentSlots.GAUNTLET
                else:
                    print(f'Missing equipment slots in wearable: {wearable_component[attribute]}')
                    raise NotImplementedError
            else:
                print(f'Missing attribute {attribute} for shield in {wearable_component}')
                raise NotImplementedError
        return wearable_attributes

    @staticmethod
    def load_weapon_raw(weapon):
        weap = dict()
        for attribute in weapon:
            if attribute == 'range':
                weap[attribute] = weapon[attribute]
            elif attribute == 'attribute':
                if weapon[attribute] == 'quickness':
                    weap[attribute] = WeaponAttributes.QUICKNESS
                elif weapon[attribute] == 'might':
                    weap[attribute] = WeaponAttributes.MIGHT
                else:
                    print(f'WeaponAttribute {weapon[attribute]} not supported in {weap}')
                    raise NotImplementedError
            elif attribute == 'min_dmg':
                weap[attribute] = weapon[attribute]
            elif attribute == 'max_dmg':
                weap[attribute] = weapon[attribute]
            elif attribute == 'hit_bonus':
                weap[attribute] = weapon[attribute]
            elif attribute == 'dmg_bonus':
                weap[attribute] = weapon[attribute]
            else:
                print(f'Missing attribute {attribute} for weapon in {weap}')
                raise NotImplementedError
        else:
            if not weap.get('min_dmg') or not weap.get('max_dmg'):
                print(f'weapon load raw: min dmg or max dmg missing in {weapon}')
                raise NotImplementedError
        return weap

    @staticmethod
    def load_attributes_raw(attributes_raw):
        attributes = dict()
        for attribute in attributes_raw:
            if attribute == 'might' or attribute == 'body' or attribute == 'wits' or attribute == 'quickness':
                attributes[attribute] = int(attributes_raw[attribute])
        return attributes

    @staticmethod
    def load_renderable_raw(renderable):
        render = dict()
        for attribute in renderable:
            # print(f'attribute for render is {attribute}')
            if attribute == "glyph":
                # print(f'attribute glyph is {item[component][attribute]}')
                render['glyph'] = renderable[attribute]
            elif attribute == "fg":
                render['fg'] = renderable[attribute]
            elif attribute == "order":
                render['order'] = RawsMaster.load_render_order(renderable[attribute])
            elif attribute == 'sprite':
                render[attribute] = renderable[attribute]
            else:
                print(f'load render raw: unknown attribute {attribute} in {renderable}')
                raise NotImplementedError
        return render

    @staticmethod
    def load_render_order(render_order_value):
        if render_order_value == 'BACKGROUND':
            return Layers.BACKGROUND
        elif render_order_value == 'MONSTER':
            return Layers.MONSTER
        elif render_order_value == 'ITEM':
            return Layers.ITEM
        else:
            print(f'render order: value {render_order_value} not supported.')
            raise NotImplementedError

    @staticmethod
    def load_skills_raw(skills_component):
        skills = dict()
        for skill in skills_component:
            # valid skill?
            if skill == 'melee':
                real_skill = Skills.MELEE
            elif skill == 'dodge':
                real_skill = Skills.DODGE
            else:
                print(f'load skills raw: Unknown skill {skill}')
                raise NotImplementedError
            skills[real_skill] = skills_component[skill]
        print(f'load skill raw: skills is {skills}')
        return skills

    @staticmethod
    def load_effects(effect_list):
        raw_effects = dict()
        for effect in effect_list:
            if effect == "provides_healing":
                raw_effects["provides_healing"] = int(effect_list[effect])
            elif effect == "damage":
                raw_effects["damage"] = int(effect_list[effect])
            elif effect == "ranged":
                raw_effects["ranged"] = int(effect_list[effect])
            elif effect == "area_of_effect":
                raw_effects["area_of_effect"] = int(effect_list[effect])
            elif effect == "confusion":
                raw_effects["confusion"] = int(effect_list[effect])
            elif effect == "particule_line":
                raw_effects["particule_line"] = parse_particule(effect_list[effect])
            elif effect == "particule":
                raw_effects["particule_line"] = parse_particule(effect_list[effect])
            elif effect == "remove_curse":
                raw_effects["remove_curse"] = True
            elif effect == "identify":
                raw_effects["identify"] = True
            else:
                print(f'load consum raw: unknown effect in {effect_list[effect]}')
                raise NotImplementedError
        return raw_effects

    @staticmethod
    def load_consumable_raw(consumable):
        raw_consumable = dict()
        for attribute in consumable:
            if attribute == 'effects':
                raw_consumable['effects'] = RawsMaster.load_effects(consumable[attribute])
            elif attribute == 'charges':
                raw_consumable['charges'] = consumable[attribute]
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
        if RawsMaster.props_index.get(name):
            print('PROP: prop found')
            return RawsMaster.create_prop(name, x, y)
        else:
            print('WARNING : Name entity not found : {name}')
        return

    @staticmethod
    def create_prop(name, x, y):
        to_create = RawsMaster.props[RawsMaster.props_index[name] - 1]
        components_for_entity = list()

        if to_create.get("name"):
            components_for_entity.append(NameComponent(to_create.get("name")))

        if to_create.get("renderable"):
            components_for_entity.append(RenderableComponent(glyph=to_create["renderable"].get('glyph'),
                                                             char_color=to_create["renderable"].get('fg'),
                                                             render_order=to_create["renderable"].get('order'),
                                                             sprite=to_create["renderable"].get('sprite')
                                                             ))

        if to_create.get("hidden"):
            components_for_entity.append(HiddenComponent())

        if to_create.get("entry_trigger"):
            components_for_entity.append(EntryTriggerComponent())
            if to_create['entry_trigger'].get('effects'):
                if to_create['entry_trigger']['effects'].get('damage'):
                    damage = InflictsDamageComponent(int(to_create['entry_trigger']['effects'].get('damage')))
                    components_for_entity.append(damage)
                if to_create['entry_trigger']['effects'].get('activations'):
                    activations = ActivationComponent(int(to_create['entry_trigger']['effects'].get('activations')))
                    components_for_entity.append(activations)

        if to_create.get("blocks_tile"):
            components_for_entity.append(BlockTileComponent())

        if to_create.get('blocks_visibility'):
            components_for_entity.append(BlockVisibilityComponent())

        if to_create.get('door_open'):
            components_for_entity.append(DoorComponent(to_create.get('door_open')))

        prop_id = World.create_entity(PositionComponent(x, y))

        for component in components_for_entity:
            World.add_component(component, prop_id)

    @staticmethod
    def create_mob(name, x, y):
        to_create = RawsMaster.mobs[RawsMaster.mob_index[name] - 1]

        components_for_entity = list()
        components_for_entity.append(MonsterComponent())
        components_for_entity.append(InitiativeComponent(config.BASE_MONSTER_INITIATIVE))

        if to_create.name:
            components_for_entity.append(NameComponent(to_create.name))

        if to_create.renderable:
            components_for_entity.append(RenderableComponent(glyph=to_create.renderable.get('glyph'),
                                                             char_color=to_create.renderable.get('fg'),
                                                             render_order=to_create.renderable.get('order'),
                                                             sprite=to_create.renderable.get('sprite')
                                                             )
                                         )

        if to_create.blocks_tile:
            components_for_entity.append(BlockTileComponent())

        if to_create.vision_range:
            components_for_entity.append(ViewshedComponent(to_create.vision_range))

        if to_create.attributes:
            mob_attr = AttributesComponent(might=to_create.attributes.get('might', 1),
                                                             body=to_create.attributes.get('body', 1),
                                                             quickness=to_create.attributes.get('quickness', 1),
                                                             wits=to_create.attributes.get('wits', 1)
                                                             )
            components_for_entity.append(mob_attr)

            # attributes needed for pv & mana
            if to_create.lvl:
                mob_lvl = to_create.lvl
            else:
                mob_lvl = 1
            mob_hp = npc_hp_at_lvl(mob_attr.body, mob_lvl)
            mob_mana = mana_point_at_level(mob_attr.wits,
                                           mob_lvl)

        if to_create.skills:
            skill_component = SkillsComponent()
            for skill in to_create.skills:
                skill_component.skills[skill] = to_create.skills[skill]
            components_for_entity.append(skill_component)

        if to_create.natural:
            natural_def_attack_component = NaturalAttackDefenseComponent(to_create.natural.get('armor', 0))

            attacks = to_create.natural.get('attacks')
            if attacks:
                for attack in attacks:
                    attack_to_create = RawsMaster.natural_attacks[RawsMaster.natural_attacks_index[attack] - 1]
                    natural_attack = NaturalAttack(
                        attack_to_create.get('name', 'Unknown attack'),
                        attack_to_create.get('attribute', WeaponAttributes.MIGHT),
                        attack_to_create.get('min_dmg', config.DEFAULT_MIN_DMG),
                        attack_to_create.get('max_dmg', config.DEFAULT_MAX_DMG),
                        attack_to_create.get('dmg_bonus', 0),
                        attack_to_create.get('hit_bonus', 0)
                    )
                    natural_def_attack_component.attacks.append(natural_attack)
            components_for_entity.append(natural_def_attack_component)

        components_for_entity.append(Pools(mob_hp, mob_mana, mob_lvl))

        mob_id = World.create_entity(PositionComponent(x, y))

        for component in components_for_entity:
            print(f'CREATE MOB: Component : {component}')
            World.add_component(component, mob_id)

        return True

    @staticmethod
    def create_item(name, x, y):
        to_create = RawsMaster.items[RawsMaster.item_index[name] - 1]

        components_for_entity = [ItemComponent()]

        if to_create.name:
            components_for_entity.append(NameComponent(to_create.name))

        if to_create.renderable:
            components_for_entity.append(RenderableComponent(glyph=to_create.renderable.get('glyph'),
                                                             char_color=to_create.renderable.get('fg'),
                                                             render_order=to_create.renderable.get('order'),
                                                             sprite=to_create.renderable.get('sprite')
                                                             )
                                         )

        if to_create.consumable:
            consumable = ConsumableComponent()

            if to_create.consumable.get('effects'):
                effect_components = RawsMaster.apply_effects(to_create.consumable.get('effects'))

                for effect_component in effect_components:
                    components_for_entity.append(effect_component)

            if to_create.consumable.get('charges'):
                consumable.charges = to_create.consumable.get('charges', 1)

            components_for_entity.append(ConsumableComponent())

        if to_create.weapon:
            components_for_entity.append(EquippableComponent(EquipmentSlots.MELEE))

            weap_attribute = to_create.weapon.get('attribute', WeaponAttributes.MIGHT)
            weap_min_dmg = to_create.weapon.get('min_dmg')
            weap_max_dmg = to_create.weapon.get('max_dmg')
            weap_dmg_bonus = to_create.weapon.get('dmg_bonus')
            weap_hit_bonus = to_create.weapon.get('hit_bonus')

            components_for_entity.append(MeleeWeaponComponent(weap_attribute, weap_min_dmg,
                                                              weap_max_dmg, weap_dmg_bonus, weap_hit_bonus))

        if to_create.wearable:
            components_for_entity.append(EquippableComponent(to_create.wearable.get('slot')))

            if to_create.wearable.get('armor'):
                components_for_entity.append(WearableComponent(to_create.wearable.get('armor')))

        if to_create.magic:
            identified_items = World.fetch('master_dungeon').identified_items
            magic_class = to_create.magic.get('class', MagicItemClass.COMMON)
            magic_naming_convention = to_create.magic.get('naming')
            magic_cursed = to_create.magic.get('cursed', False)

            # si nom inconnu, on utilise l'obfuscation
            if name not in identified_items:
                if magic_naming_convention == 'scroll':
                    scroll_names = World.fetch('master_dungeon').scroll_mappings
                    components_for_entity.append(ObfuscatedNameComponent(scroll_names.get(name)))
                elif magic_naming_convention == 'potion':
                    potion_names = World.fetch('master_dungeon').potion_mappings
                    components_for_entity.append(ObfuscatedNameComponent(potion_names.get(name)))
                else:
                    components_for_entity.append(ObfuscatedNameComponent(magic_naming_convention))

            components_for_entity.append(MagicItemComponent(magic_class=magic_class,
                                                            naming=magic_naming_convention,
                                                            cursed=magic_cursed))

            if magic_cursed:
                components_for_entity.append(CursedItemComponent())

        if to_create.attributes:
            components_for_entity.append(AttributeBonusComponent(
                might=to_create.attributes.get('might'),
                body=to_create.attributes.get('body'),
                quickness=to_create.attributes.get('quickness'),
                wits=to_create.attributes.get('wits')
            ))

        item_id = World.create_entity(PositionComponent(x, y))
        for component in components_for_entity:
            World.add_component(component, item_id)

        return True

    @staticmethod
    def apply_effects(effects):
        effects_list = list()
        if effects.get('provides_healing'):
            effects_list.append(ProvidesHealingComponent(effects.get('provides_healing')))

        if effects.get('damage'):
            effects_list.append(InflictsDamageComponent(effects.get('damage')))

        if effects.get('ranged'):
            effects_list.append(RangedComponent(effects.get('ranged')))

        if effects.get('area_of_effect'):
            effects_list.append(AreaOfEffectComponent(effects.get('area_of_effect')))

        if effects.get('confusion'):
            effects_list.append(ConfusionComponent())
            effects_list.append(DurationComponent(effects.get('confusion')))

        if effects.get('particule'):
            particule_infos = effects.get('particule')
            effects_list.append(SpawnParticuleBurstComponent(particule_infos['glyph'],
                                                                      particule_infos['color'],
                                                                      particule_infos['sprite']))

        if effects.get('particule_line'):
            particule_infos = effects.get('particule_line')
            effects_list.append(SpawnParticuleLineComponent(particule_infos['glyph'],
                                                                     particule_infos['color'],
                                                                     particule_infos['sprite']))

        if effects.get('remove_curse'):
            effects_list.append(ProvidesCurseRemovalComponent())

        if effects.get('identify'):
            effects_list.append(ProvidesIdentificationComponent())

        return effects_list

    @staticmethod
    def get_scroll_tags():
        result = list()
        for item in RawsMaster.items:
            if item.magic.get('naming') == 'scroll':
                result.append(item.name)
        return result

    @staticmethod
    def get_potion_tags():
        result = list()
        for item in RawsMaster.items:
            if item.magic.get('naming') == 'potion':
                result.append(item.name)
        return result

    @staticmethod
    def is_tag_magic(tag):
        magic_tag = RawsMaster.item_index.get(tag)
        if magic_tag:
            item = RawsMaster.items[RawsMaster.item_index[tag] - 1]
            return item.magic
        return False
