from bearlibterminal import terminal

from ui_system.interface import GraphicalModes, Interface
from ui_system.render_menus import draw_background
from ui_system.render_functions import get_item_color, get_item_display_name, print_shadow
from world import World
from components.obfuscated_name_component import ObfuscatedNameComponent
from components.consumable_component import ConsumableComponent
from components.provides_healing_component import ProvidesHealingComponent
from components.items_component import MeleeWeaponComponent
from components.equipped_component import EquippedComponent
from components.area_effect_component import AreaOfEffectComponent
from components.confusion_component import ConfusionComponent
from components.equippable_component import EquippableComponent
from components.inflicts_damage_component import InflictsDamageComponent
from components.magic_item_component import MagicItemComponent
from components.ranged_component import RangedComponent
from systems.inventory_system import get_equipped_items, get_items_in_inventory
from ui_system.ui_enums import Layers
import config
from texts import Texts


class Menu:
    pass


class InventoryMenu:
    def __init__(self, header):
        self.header = header
        self.selected_item = None
        self.window_x = config.SCREEN_WIDTH // 8
        self.window_y = config.SCREEN_HEIGHT // 8
        self.window_end_x = self.window_x * 7
        self.window_end_y = self.window_y * 7   # default
        self.total_width = (self.window_end_x - self.window_x)
        self.letter_index = ord('a')
        self.menu_contents = list()

    def initialize(self):
        print(f'inventory: initialize')
        # header (Traduction, sans couleurs)
        # top: item selectionné
        # left: item list
        # right: description
        # bottom: options for selected item
        # end : how to quit
        user = World.fetch('player')
        items_to_display = get_items_in_inventory(user)
        equipped = get_equipped_items(user)
        decorated_names_list = self.get_decorated_names_list(items_to_display, equipped)
        self.create_menu_content(decorated_names_list)
        self.render_menu()

    def get_decorated_names_list(self, items_to_display, equipped):
        item_list_max_width = (self.window_end_x - self.window_x) // 2
        decorated_names_list = list()
        for item in items_to_display:
            item_name, equipped_info = self.reduce_item_option(item_list_max_width, item, equipped)
            # on ajoute la couleur de l'item + letter_index si pas d'items selectionnés
            if self.selected_item:
                color = config.COLOR_INFO_UNSELECTABLE_ITEMS_INVENTORY
                letter_index = '(-)'
            else:
                color = get_item_color(item)
                letter_index = f'({chr(self.letter_index)})'

            final_msg = f'[color={color}]{letter_index} {equipped_info} {item_name}[/color]'
            decorated_names_list.append(final_msg)

            if not self.selected_item:
                # on augmente l'index car on va choisir dans cette liste.
                self.letter_index += 1
        return decorated_names_list

    def reduce_item_option(self, total_width, item, equipped):
        chars_to_cut = 0
        # we need : letter_index + equipped_info + item_name
        item_name = Texts.get_text(get_item_display_name(item))
        if item in equipped:
            equipped_info = f'({Texts.get_text("EQUIPPED")})'
        else:
            equipped_info = ''
        final_msg = f'{chr(self.letter_index)}) {equipped_info} {item_name}'
        if len(final_msg) > total_width:
            chars_to_cut = total_width - len(final_msg)

        while chars_to_cut > 0:
            # on coupe d'abord equipped info:
            if len(equipped_info) > 3:
                equipped_info = {Texts.get_text("EQUIPPED")}[:1]
                equipped_info = f'({equipped_info})'
                final_msg = f'{self.letter_index}){equipped_info}{item_name}'
                if len(final_msg) > total_width:
                    chars_to_cut = total_width - len(final_msg)
            elif len(item_name) > 6:
                item_name = item_name[:6]
            else:
                # plus rien a faire possible.
                break
        return item_name, equipped_info

    def cut_text_in_lines_according_width(self, full_text, width):
        if not full_text:
            lines_list = ['']
            return lines_list

        full_text_width = len(full_text)
        full_text = full_text.split()
        lines_list = list()
        line = ''
        while full_text_width >= width:
            while len(line + full_text[0] + ' ') < width:
                line += full_text[0] + ' '
                full_text.remove(full_text[0])
                full_text_width -= len(full_text[0] + ' ')
            lines_list.append(line)
            line = ''
        # s'il reste du texte avec taille < width
        for word in full_text:
            line += word + ' '
        lines_list.append(line)

        return lines_list

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

    def create_menu_content(self, decorated_names_list):
        print(f'inventory: create menu content')
        # content = (x, y, text)
        menu_contents = list()

        # variables
        mutable_y = self.window_y
        mutable_y_right = self.window_y

        # header
        center_header_start = ((self.window_end_x - len(self.header)) // 2)  # + window_x
        header = f'[color={config.COLOR_SYS_MSG}] {self.header} [/color]'  # On ajoute la couleur après le len()
        menu_contents.append((center_header_start, mutable_y, header))
        mutable_y += 3
        mutable_y_right += 3

        # selected item
        if self.selected_item:
            selected_content = Texts.get_text(get_item_display_name(self.selected_item))
        else:
            selected_content = Texts.get_text('INVENTORY_USAGE_EXPLANATION')
        center_selected_item_start = ((self.window_end_x - len(selected_content)) // 2)  # + window_x
        selected_content = f'[color={config.COLOR_INFO_INVENTORY_SELECTED_ITEM}] {selected_content} [/color]'
        menu_contents.append((center_selected_item_start, mutable_y, selected_content))
        mutable_y += 3
        mutable_y_right += 3

        # left: item list.
        if not decorated_names_list:
            menu_contents.append((self.window_x, mutable_y, Texts.get_text('NO_ITEM_INVENTORY')))
        for decorated_name in decorated_names_list:
            menu_contents.append((self.window_x, mutable_y, decorated_name))
            mutable_y += 1

        # right: description
        if self.selected_item:
            item_description_width_total = (self.window_end_x - self.window_x) // 2
            item_description_width_start = self.window_x + item_description_width_total

            info_title = f'[color={config.COLOR_SYS_MSG}]{Texts.get_text("ITEM_INFO")}[/color]'
            menu_contents.append((item_description_width_start, mutable_y_right, info_title))
            mutable_y_right += 2

            # on recupere les infos.
            item_obfuscate = World.get_entity_component(self.selected_item, ObfuscatedNameComponent)
            if item_obfuscate:
                obfuscate = True
            else:
                obfuscate = False
            color = config.COLOR_INFO_INVENTORY_TEXT

            if obfuscate:
                print(f'menu: item obfuscate')
                full_text = self.cut_text_in_lines_according_width(
                    Texts.get_text("CANT_KNOW_WITHOUT_USAGE_OR_IDENTIFICATION"),
                    item_description_width_total)

                for line in full_text:
                    menu_contents.append((item_description_width_start, mutable_y_right,
                                          f'[color={color}]{line}[/color]'))
                    mutable_y_right += 1
            mutable_y_right += 2

            # Some infos can be displayed, even if obfuscate
            color = config.COLOR_INFO_ATTRIBUTE_INVENTORY_MENU
            item_attribute_list = self.get_item_description(self.selected_item, obfuscate)
            for item_attribute in item_attribute_list:
                menu_contents.append((item_description_width_start,
                                      mutable_y_right,
                                      f'[color={color}]{item_attribute}[/color]'))
                mutable_y_right += 1

            # bottom: options if any.
            mutable_y = max(mutable_y, mutable_y_right)
            mutable_y += 3

            if self.selected_item:
                mutable_x = self.window_x + 2   # margin
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
                    menu_contents.append((mutable_x, mutable_y,
                                          f'[color={config.COLOR_INVENTORY_OPTION}]{option}[/color]'))
                    mutable_x += large_width
                    if mutable_x + large_width >= self.window_end_x:
                        mutable_x = self.window_x + 2   # margin
                        mutable_y += 1
        mutable_y += 3

        # end : how to quit.
        exit_text = f' {Texts.get_text("ESCAPE_TO_CANCEL")} '
        center_exit_text_x = ((self.window_end_x - len(exit_text)) // 2)  # + window_x
        exit_text = f'[color=darker yellow]{exit_text}[/color]'
        menu_contents.append((center_exit_text_x, mutable_y, exit_text))

        self.menu_contents = menu_contents
        self.window_end_y = mutable_y

    def render_menu(self):
        print(f'inventory: render menu: self menu contents : {self.menu_contents}')
        terminal.layer(Layers.MENU.value)
        for x, y, content in self.menu_contents:
            print(f'render menu : {x, y, content}')
            print_shadow(x, y, content)

        if Interface.mode == GraphicalModes.TILES:
            draw_background(self.window_x, self.window_y, self.window_end_x, self.window_end_y)
        terminal.refresh()
