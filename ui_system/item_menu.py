from enum import Enum

from ui_system.menus import Menu, BoxMenu, MenuAlignement
from ui_system.render_functions import get_item_color, get_item_display_name
from world import World
from components.name_components import ObfuscatedNameComponent
from components.provide_effects_components import ProvidesHealingComponent
from components.item_components import MeleeWeaponComponent, ConsumableComponent
from components.equip_components import EquippedComponent, EquippableComponent
from components.area_effect_component import AreaOfEffectComponent
from components.confusion_component import ConfusionComponent
from components.inflicts_damage_component import InflictsDamageComponent
from components.magic_item_components import MagicItemComponent
from components.ranged_component import RangedComponent
from inventory_system.inventory_functions import get_non_identify_items_in_inventory, get_items_in_inventory, \
    get_known_cursed_items_in_inventory
import config
from texts import Texts


class ItemMenuType(Enum):
    REMOVAL_CURSE_ON_ITEM = 0
    IDENTIFY_ITEM = 1
    INVENTORY_MENU = 2
    INVENTORY_WITH_SELECT_ITEM_MENU = 3


class ItemMenu(Menu):
    """ Generic Menu with list of items.
    List is requested in get_item_list_according_to_type"""
    def __init__(self, header, type):
        super().__init__(header)
        self.type = type
        self.explanation_text = self.get_explanation_text()
        self.no_item_text = self.get_no_item_text()

    def get_no_item_text(self):
        if self.type == ItemMenuType.IDENTIFY_ITEM:
            return 'ALL_ITEMS_ARE_IDENTIFIED'
        elif self.type == ItemMenuType.REMOVAL_CURSE_ON_ITEM:
            return "NO_CURSE_ITEM_KNOWN"
        elif self.type == ItemMenuType.INVENTORY_MENU:
            return "NO_ITEM_INVENTORY"
        elif self.type == ItemMenuType.INVENTORY_WITH_SELECT_ITEM_MENU:
            return "NO_ITEM_INVENTORY"

    def get_explanation_text(self):
        if self.type == ItemMenuType.IDENTIFY_ITEM:
            return 'IDENTIFY_EXPLANATION'
        elif self.type == ItemMenuType.REMOVAL_CURSE_ON_ITEM:
            return "CURSE_REMOVAL_EXPLANATION"
        elif self.type == ItemMenuType.INVENTORY_MENU:
            return "INVENTORY_USAGE_EXPLANATION"
        elif self.type == ItemMenuType.INVENTORY_WITH_SELECT_ITEM_MENU:
            return "INVENTORY_USAGE_EXPLANATION"

    def get_item_list_according_to_type(self, user):
        item_list = list()
        if self.type == ItemMenuType.IDENTIFY_ITEM:
            item_list = get_non_identify_items_in_inventory(user)
        elif self.type == ItemMenuType.REMOVAL_CURSE_ON_ITEM:
            item_list = get_known_cursed_items_in_inventory(user)
        elif self.type == ItemMenuType.INVENTORY_MENU:
            item_list = get_items_in_inventory(user)
        elif self.type == ItemMenuType.INVENTORY_WITH_SELECT_ITEM_MENU:
            item_list = get_items_in_inventory(user)
        return item_list

    def initialize(self):
        user = World.fetch('player')
        items_to_display = self.get_item_list_according_to_type(user)
        decorated_names_list = self.get_decorated_names_list(items_to_display)
        self.create_menu_content(decorated_names_list)
        self.render_menu()

    def get_decorated_names_list(self, items_to_display):
        decorated_names_list = list()
        for item in items_to_display:
            item_name, equipped_info = self.display_name(item)
            color = get_item_color(item)
            letter_index = f'({chr(self.letter_index)})'

            final_msg = f'[color={color}]{letter_index} {equipped_info} {item_name}[/color]'
            decorated_names_list.append(final_msg)

            # on augmente l'index car on va choisir dans cette liste.
            self.letter_index += 1

        return decorated_names_list

    def display_name(self, item):
        item_name = Texts.get_text(get_item_display_name(item))
        item_equipped = World.get_entity_component(item, EquippedComponent)
        if item_equipped:
            equipped_info = f'({Texts.get_text("EQUIPPED")})'
        else:
            equipped_info = ''
        return item_name, equipped_info

    def create_menu_content(self, decorated_names_list):
        print(f'ItemMenu: create menu content for {self.type}')
        # content = (x, y, text)
        menu_contents = list()
        render_order = 1

        # header
        box = BoxMenu(render_order, linebreak=3, margin=1)
        render_order += 1
        header = f'[color={config.COLOR_SYS_MSG}] {self.header} [/color]'  # On ajoute la couleur après le len()
        box.add(header, MenuAlignement.CENTER)
        menu_contents.append(box)

        # usage explanation
        box = BoxMenu(render_order)
        render_order += 1
        selected_content = Texts.get_text(self.explanation_text)
        selected_content = f'[color={config.COLOR_INFO_INVENTORY_SELECTED_ITEM}] {selected_content} [/color]'
        box.add(selected_content, MenuAlignement.CENTER)
        menu_contents.append(box)

        # item list.
        box = BoxMenu(render_order)
        render_order += 1
        if not decorated_names_list:
            box.add(Texts.get_text(self.no_item_text), MenuAlignement.CENTER)

        for decorated_name in decorated_names_list:
            box.add(decorated_name, MenuAlignement.CENTER)
        menu_contents.append(box)

        # end : how to quit.
        box = BoxMenu(render_order)
        render_order += 1

        exit_text = f' {Texts.get_text("ESCAPE_TO_CANCEL")} '
        exit_text = f'[color=darker yellow]{exit_text}[/color]'
        box.add(exit_text, MenuAlignement.CENTER)
        menu_contents.append(box)

        self.menu_contents = menu_contents


class InventorySelectedMenu(ItemMenu):
    def __init__(self, header, type, selected_item):
        super().__init__(header, type)
        self.selected_item = selected_item

    def create_menu_content(self, decorated_names_list):
        print(f'inventory: create menu content')
        # content = (x, y, text)
        menu_contents = list()
        render_order = 1

        # header
        box = BoxMenu(render_order, linebreak=3, margin=1)
        render_order += 1
        header = f'[color={config.COLOR_SYS_MSG}] {self.header} [/color]'  # On ajoute la couleur après le len()
        box.add(header, MenuAlignement.CENTER)
        menu_contents.append(box)

        # selected item
        box = BoxMenu(render_order)
        render_order += 1
        selected_content = Texts.get_text(self.explanation_text)
        selected_content = f'[color={config.COLOR_INFO_INVENTORY_SELECTED_ITEM}] {selected_content} [/color]'
        box.add(selected_content, MenuAlignement.CENTER)
        menu_contents.append(box)

        # left: item list.
        box = BoxMenu(render_order)
        render_order += 1
        if not decorated_names_list:
            box.add(Texts.get_text(self.no_item_text), MenuAlignement.CENTER)
        for decorated_name in decorated_names_list:
            box.add(decorated_name, MenuAlignement.CENTER)
        menu_contents.append(box)

        # right: description
        box = BoxMenu(render_order)
        render_order += 1

        info_title = f'[color={config.COLOR_SYS_MSG}]{Texts.get_text("ITEM_INFO")}[/color]'
        box.add(info_title, MenuAlignement.CENTER)

        # on recupere les infos.
        item_obfuscate = World.get_entity_component(self.selected_item, ObfuscatedNameComponent)
        if item_obfuscate:
            obfuscate = True
        else:
            obfuscate = False
        color = config.COLOR_INFO_INVENTORY_TEXT

        if obfuscate:
            full_text = Texts.get_text("CANT_KNOW_WITHOUT_USAGE_OR_IDENTIFICATION")
            box.add(f'[color={color}]{full_text}[/color]', MenuAlignement.CENTER)
        menu_contents.append(box)

        box = BoxMenu(render_order)
        render_order += 1
        # Some infos can be displayed, even if obfuscate
        color = config.COLOR_INFO_ATTRIBUTE_INVENTORY_MENU
        item_attribute_list = self.get_item_description(self.selected_item, obfuscate)
        for item_attribute in item_attribute_list:
            box.add(f'[color={color}]{item_attribute}[/color]', MenuAlignement.CENTER)
        menu_contents.append(box)

        # bottom: options if any.
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1

        available_options = self.get_item_available_options(self.selected_item)

        decorated_options = list()
        for option in available_options:
            decorated_options.append(f'({chr(self.letter_index)}) {option}')
            self.letter_index += 1

        # get the longest option
        large_width = 0
        for option in decorated_options:
            if len(option) > large_width:
                large_width = len(option)
        large_width += 3

        for option in decorated_options:
            box.add(f'[color={config.COLOR_INVENTORY_OPTION}]{option}[/color]',
                    MenuAlignement.CENTER)
        menu_contents.append(box)

        # end : how to quit.
        box = BoxMenu(render_order)
        render_order += 1
        if self.selected_item:
            exit_text = f' {Texts.get_text("ESCAPE_TO_CHOOSE_OTHER_ITEM")} '
        else:
            exit_text = f' {Texts.get_text("ESCAPE_TO_CANCEL")} '
        exit_text = f'[color=darker yellow]{exit_text}[/color]'
        box.add(exit_text, MenuAlignement.CENTER)
        menu_contents.append(box)

        self.menu_contents = menu_contents

    def get_item_available_options(self, item):
        item_weapon = World.get_entity_component(item, MeleeWeaponComponent)
        item_equipped = World.get_entity_component(item, EquippedComponent)

        available_options = list()
        if item_weapon:
            if item_equipped:
                available_options.append(Texts.get_text('UNEQUIP_ITEM'))
            else:
                available_options.append(Texts.get_text('EQUIP_ITEM'))
        else:
            available_options.append(Texts.get_text('USE_ITEM'))
        available_options.append(Texts.get_text('DROP_ITEM'))

        return available_options

    def get_item_description(self, item, obfuscate=False):
        item_description = list()

        item_consumable = World.get_entity_component(item, ConsumableComponent)
        item_provide_healing = World.get_entity_component(item, ProvidesHealingComponent)
        item_melee_weapon = World.get_entity_component(item, MeleeWeaponComponent)
        item_area_effect = World.get_entity_component(item, AreaOfEffectComponent)
        item_confusion = World.get_entity_component(item, ConfusionComponent)
        item_equippable = World.get_entity_component(item, EquippableComponent)
        item_inflict_dmg = World.get_entity_component(item, InflictsDamageComponent)
        item_magic = World.get_entity_component(item, MagicItemComponent)
        item_ranged = World.get_entity_component(item, RangedComponent)

        if item_magic:
            item_description.append(Texts.get_text("ITEM_INFO_MAGIC"))

        if item_inflict_dmg and not obfuscate:
            item_description.append(Texts.get_text("ITEM_INFO_INFLICT_DMG"))

        if item_provide_healing and not obfuscate:
            item_description.append(Texts.get_text("ITEM_INFO_HEALING"))

        if item_equippable:
            # has equipment slot
            item_description.append(Texts.get_text("ITEM_INFO_EQUIPPABLE"))

        if item_ranged and not obfuscate:
            item_description.append(Texts.get_text("ITEM_INFO_RANGED").format(item_ranged.range))

        if item_area_effect and not obfuscate:
            item_description.append(Texts.get_text("ITEM_INFO_AREA_EFFECT").format(item_area_effect.radius))

        if item_confusion and not obfuscate:
            item_description.append(Texts.get_text("ITEM_INFO_CONFUSION"))

        if item_consumable:
            item_description.append(Texts.get_text("ITEM_INFO_CONSUMABLE"))

        if item_melee_weapon:
            item_description.append(Texts.get_text("ITEM_INFO_MELEE_WEAPON"))

        return item_description
