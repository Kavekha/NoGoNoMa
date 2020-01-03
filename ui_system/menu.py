from bearlibterminal import terminal

from ui_system.interface import GraphicalModes, Interface
from ui_system.render_menus import draw_tile_menu, draw_ascii_menu, draw_background
from ui_system.render_functions import get_item_color, get_item_display_name, print_shadow
from world import World
from components.attributes_component import AttributesComponent
from components.pools_component import Pools
from systems.inventory_system import get_equipped_items, get_items_in_inventory
from ui_system.ui_enums import Layers
from player_systems.game_system import xp_for_next_level
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
            # on ajoute la couleur de l'item
            final_msg = f'[color={get_item_color(item)}]({chr(self.letter_index)}) {equipped_info} {item_name}[/color]'
            decorated_names_list.append(final_msg)
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

    def cut_name_line_by_line(self, text, width):
        unknown_item_msg = text
        full_text = list()
        while len(unknown_item_msg) > width:
            line = full_text[0: width - 2]
            full_text.append(line)
            unknown_item_msg = unknown_item_msg[width - 1:]
        if not full_text:
            full_text.append(unknown_item_msg)
        return full_text

    def get_item_available_options(self, item):
        available_options = [
            Texts.get_text('USE_ITEM'),
            Texts.get_text('DROP_ITEM'),
            Texts.get_text('EQUIP_ITEM'),
            Texts.get_text('UNEQUIP_ITEM')
        ]
        return available_options

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
        mutable_y += 2
        mutable_y_right += 2

        # selected item
        if self.selected_item:
            selected_content = Texts.get_text(get_item_display_name(self.selected_item))
        else:
            selected_content = Texts.get_text('INVENTORY_USAGE_EXPLANATION')
        center_selected_item_start = ((self.window_end_x - len(selected_content)) // 2)  # + window_x
        selected_content = f'[color={config.COLOR_SYS_MSG}] {selected_content} [/color]'
        menu_contents.append((center_selected_item_start, mutable_y, selected_content))
        mutable_y += 2
        mutable_y_right += 2

        # left: item list.
        for decorated_name in decorated_names_list:
            menu_contents.append((self.window_x, mutable_y, decorated_name))
            mutable_y += 1

        # right: description
        if self.selected_item:
            from components.obfuscated_name_component import ObfuscatedNameComponent
            from components.consumable_component import ConsumableComponent
            from components.provides_healing_component import ProvidesHealingComponent
            from components.items_component import MeleeWeaponComponent

            # on recupere les infos.
            item_obfuscate = World.get_entity_component(self.selected_item, ObfuscatedNameComponent)
            item_consumable = World.get_entity_component(self.selected_item, ConsumableComponent)
            item_provide_healing = World.get_entity_component(self.selected_item, ProvidesHealingComponent)
            item_melee_weapon = World.get_entity_component(self.selected_item, MeleeWeaponComponent)

            item_description_width_total = (self.window_end_x - self.window_x) // 2
            item_description_width_start = self.window_x + item_description_width_total

            info_title = f'[color={config.COLOR_SYS_MSG}]{Texts.get_text("ITEM_INFO")}[/color]'
            menu_contents.append((item_description_width_start, mutable_y_right, info_title))
            mutable_y_right += 2

            if item_obfuscate:
                full_text = self.cut_name_line_by_line(Texts.get_text("INVENTORY_USAGE_EXPLANATION"),
                                                       item_description_width_total)

                for line in full_text:
                    menu_contents.append((item_description_width_start, mutable_y_right, line))
                    mutable_y_right += 1
            else:
                if item_consumable:
                    menu_contents.append((item_description_width_start, mutable_y_right,
                                 f'{Texts.get_text("ITEM_INFO_CONSUMMABLE")}'))
                    mutable_y_right += 1
                if item_provide_healing:
                    menu_contents.append((item_description_width_start, mutable_y_right,
                                 f'{Texts.get_text("ITEM_INFO_HEALING")}'))
                    mutable_y_right += 1
                if item_melee_weapon:
                    menu_contents.append((item_description_width_start, mutable_y_right,
                                 f'{Texts.get_text("ITEM_INFO_MELEE_WEAPON")}'))
                    mutable_y_right += 1

            # bottom: options if any.
            if self.selected_item:
                mutable_x = self.window_x
                available_options = self.get_item_available_options(self.selected_item)

                large_width = 0
                for option in available_options:
                    if len(option) > large_width + 3:
                        large_width = len(option)

                for option in available_options:
                    menu_contents.append((mutable_x, mutable_y, option))
                    mutable_x += large_width
                    if mutable_x >= self.window_end_x:
                        mutable_x = self.window_x
                        mutable_y += 1
        mutable_y += 5

        # end : how to quit.
        exit_text = f' {Texts.get_text("ESCAPE_TO_CANCEL")} '
        center_exit_text_x = ((self.window_end_x - len(exit_text)) // 2)  # + window_x
        exit_text = f'[color=darker yellow]{exit_text}[/color]'
        menu_contents.append((center_exit_text_x, mutable_y, exit_text))

        self.menu_contents = menu_contents
        self.window_end_y = mutable_y

    def render_menu(self):
        print(f'inventory: render menu')
        terminal.layer(Layers.MENU.value)
        for x, y, content in self.menu_contents:
            print(f'render menu : {x, y, content}')
            print_shadow(x, y, content)

        if Interface.mode == GraphicalModes.TILES:
            draw_background(self.window_x, self.window_y, self.window_end_x, self.window_end_y)
        terminal.refresh()
