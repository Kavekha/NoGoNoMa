import json
import os

from components.skills_component import Skills

from data.components_enum import EquipmentSlots, WeaponAttributes, MagicItemClass
from data_raw_master.raws_structs import RawsSpawnTable
from data_raw_master.load_raws import parse_particule
from ui_system.ui_enums import Layers
import config


class RawCompendium:
    """ Tous les Raws sont convertis dans un dictionnaire geant selon chaque categorie.
    Ce dictionnaire est consulté par RawCompendium ensuite pour créer des entités réelles.

    Etapes:
        Load raws:
            On load chaque fichier json trouvé
        Load raw:
            On regarde data si item, props, mob, spawn_table
        Load data raw:
            On load la data selon sa propre methode, si item, props, etc
        Load index:
            On créé un index pour tous les objets pour les retrouver plus facilement."""
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
    def load_raws():
        print(f'------- load raws ------')
        full_path = os.getcwd() + config.RAW_FILES  # game
        # full_path = '../raws'

        for file in os.listdir(full_path):
            RawCompendium.load_raw(file)
        print(f'---- raws loaded -------')

        print(f'---- Create index -----')
        RawCompendium.load_index()

    @staticmethod
    def load_index():
        for i, item in enumerate(RawCompendium.items):
            RawCompendium.item_index[item["name"]] = i + 1

        for i, mob in enumerate(RawCompendium.mobs):
            RawCompendium.mob_index[mob["name"]] = i + 1

        for i, attack in enumerate(RawCompendium.natural_attacks):
            RawCompendium.natural_attacks_index[attack["name"]] = i + 1

        for i, prop in enumerate(RawCompendium.props):
            RawCompendium.props_index[prop["name"]] = i + 1

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
                    RawCompendium.load_item_raw(datas[data])
                elif data == 'mobs':
                    RawCompendium.load_mob_raw(datas[data])
                elif data == 'spawn_table':
                    RawCompendium.load_spawn_table_raw(datas[data])
                elif data == 'natural_attacks':
                    RawCompendium.load_natural_attacks_raw(datas[data])
                elif data == 'props':
                    RawCompendium.load_props_raw(datas[data])
                else:
                    print(f'load raw: Data type {data} not supported')
                    raise NotImplementedError

    @staticmethod
    def load_item_raw(data):
        print(f'---- load item ---')
        for item in data:
            raw_item = dict()
            for component in item:
                if component == 'name':
                    raw_item[component] = item[component]
                elif component == 'renderable':
                    raw_item[component] = RawCompendium.load_renderable_raw(item[component])
                elif component == 'consumable':
                    raw_item[component] = RawCompendium.load_consumable_raw(item[component])
                elif component == 'weapon':
                    raw_item[component] = RawCompendium.load_weapon_raw(item[component])
                elif component == 'wearable':
                    raw_item[component] = RawCompendium.load_wearable_raw(item[component])
                elif component == 'magic':
                    raw_item[component] = RawCompendium.load_magic_item_raw(item[component])
                elif component == 'attributes':
                    raw_item[component] = RawCompendium.load_attributes_bonus_raw(item[component])
                else:
                    print(f'load item raw: unkown component in {component}')
                    raise NotImplementedError
            RawCompendium.items.append(raw_item)

    @staticmethod
    def load_mob_raw(data):
        print(f'---- load mob ---')
        for mob in data:
            raw_mob = dict()
            for component in mob:
                if component == 'name':
                    raw_mob[component] = mob[component]
                elif component == 'renderable':
                    raw_mob[component] = RawCompendium.load_renderable_raw(mob[component])
                elif component == 'blocks_tile':
                    raw_mob[component] = mob[component]
                elif component == 'vision_range':
                    raw_mob[component] = int(mob[component])
                elif component == 'attributes':
                    raw_mob[component] = RawCompendium.load_attributes_raw(mob[component])
                elif component == 'skills':
                    raw_mob[component] = RawCompendium.load_skills_raw(mob[component])
                elif component == 'level':
                    raw_mob[component] = mob[component]
                elif component == 'natural':
                    raw_mob[component] = RawCompendium.load_natural_def_attack_raw(mob[component])
                else:
                    print(f'Unknown component {component} for mob {mob}')
                    raise NotImplementedError
            RawCompendium.mobs.append(raw_mob)

    @staticmethod
    def load_props_raw(data):
        for prop_raw in data:
            props = {}
            for component in prop_raw:
                if component == 'name':
                    props[component] = prop_raw[component]
                elif component == 'renderable':
                    props[component] = RawCompendium.load_renderable_raw(prop_raw[component])
                elif component == 'hidden':
                    props[component] = prop_raw[component]
                elif component == 'entry_trigger':
                    props[component] = prop_raw[component]
                elif component == 'blocks_tile':
                    props[component] = prop_raw[component]
                elif component == 'blocks_visibility':
                    props[component] = prop_raw[component]
                elif component == 'door_close':
                    props[component] = prop_raw[component]
                else:
                    print(f'prop component {component} is not implemented for props')
                    raise NotImplementedError
            RawCompendium.props.append(props)

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
            RawCompendium.natural_attacks.append(natural_attack)

    @staticmethod
    def load_spawn_table_raw(data):
        print(f'--- load spawn tables ---')
        raw_table = RawsSpawnTable()
        for spawn_entry in data:
            object_entry = {}
            name = None
            for info in spawn_entry:
                if info == 'name' and not object_entry:
                    name = spawn_entry[info]
                elif info == 'weight' and name:
                    object_entry[info] = int(spawn_entry[info])
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
        RawCompendium.spawn_table.append(raw_table)

    @staticmethod
    def load_natural_def_attack_raw(data):
        naturals = {}
        for natural in data:
            if natural == 'armor':
                naturals[natural] = data[natural]
            elif natural == 'attacks':
                naturals[natural] = RawCompendium.load_mob_natural_attacks_raw(data[natural])
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
            else:
                print(f'attribute {attribute} not supported in load attributes raw')
                raise NotImplementedError
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
                render['order'] = RawCompendium.load_render_order(renderable[attribute])
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
                raw_consumable['effects'] = RawCompendium.load_effects(consumable[attribute])
            elif attribute == 'charges':
                raw_consumable['charges'] = consumable[attribute]
            else:
                print(f'load consumable raw: unkown attribute in {consumable}')
                raise NotImplementedError
        return raw_consumable
