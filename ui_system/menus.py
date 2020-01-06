from bearlibterminal import terminal

from itertools import product as it_product
from enum import Enum

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
from components.attributes_component import AttributesComponent
from components.pools_component import Pools
from components.skills_component import SkillsComponent, Skills
from systems.inventory_system import get_equipped_items, get_items_in_inventory
from player_systems.game_system import xp_for_next_level
from ui_system.ui_enums import Layers
from ui_system.text_functions import remove_color_tag
import config
from texts import Texts


class MenuAlignement(Enum):
    CENTER = 0
    LEFT = 1
    RIGHT = 2


class BoxMenu:
    def __init__(self, render_order=100, linebreak=0):
        self.content = list()
        self.render_order = render_order
        self.linebreak = linebreak

    def get_height(self):
        height = 0
        for _content in self.content:
            height += 1
        return height

    def get_total_height(self):
        # with line break
        height = 0
        for _content in self.content:
            height += 1
        height += self.linebreak
        return height

    def add(self, text, alignement):
        self.content.append((text, alignement))

    def get_center_point(self, width, len_text):
        center_x = (width - len_text) // 2
        return center_x

    def paste_on_window(self, x, y, width):
        mut_y = y
        max_y = len(self.content)
        previous_color = terminal.color(terminal.TK_COLOR)
        draw_background(x, y - 1, width + x, y + max_y, config.COLOR_MENU_BACKGROUND_BASE)
        terminal.color(previous_color)
        for content, alignement in self.content:
            cx = 0
            if alignement == MenuAlignement.CENTER:
                content_without_color = remove_color_tag(content)
                cx = self.get_center_point(width, len(content_without_color))
            print_shadow(cx + x, mut_y, content)
            mut_y += 1


class Menu:
    def __init__(self, header):
        self.header = header
        # 3/4 menu width & height
        margin = config.SCREEN_WIDTH // 4
        self.window_x = 0
        self.window_end_x = config.SCREEN_WIDTH - margin
        self.window_y = 0
        self.window_end_y = 0
        self.total_width = (self.window_end_x - self.window_x)
        self.letter_index = ord('a')
        self.menu_contents = list()

    def menu_placement(self):
        # center for now
        start_x = (config.SCREEN_WIDTH - self.window_end_x) // 2
        start_y = (config.SCREEN_HEIGHT - self.window_end_y) // 2
        self.window_x = start_x
        self.window_y = start_y
        self.window_end_x += start_x
        self.window_end_y += start_y

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

    def render_menu(self):
        terminal.layer(Layers.MENU.value)
        self.menu_placement()
        height = 0
        for content in self.menu_contents:
            height += content.get_total_height()
        draw_background(self.window_x, self.window_y, self.window_end_x, self.window_y + height, color='gray')
        y = self.window_y

        self.menu_contents = sorted(self.menu_contents, key=lambda cont: cont.render_order)
        for content in self.menu_contents:
            width = self.window_end_x - self.window_x
            content.paste_on_window(self.window_x, y, width)
            y += content.get_height()
            y += content.linebreak

        terminal.refresh()

    def get_x_for_center_text(self, x, width, text):
        if x + width > self.window_end_x:
            width = self.window_end_x - x
        center = (width - len(text)) // 2
        center += x
        return center


class MainMenu(Menu):
    def initialize(self):
        self.create_content()
        self.render_menu()

    def create_content(self):
        menu_contents = list()
        mutable_y = self.window_y + 1
        render_order = 1

        # HEADER
        box = BoxMenu(render_order, linebreak=5)
        color = config.COLOR_MAIN_MENU_TITLE
        center_start = self.get_x_for_center_text(self.window_x, self.window_end_x, self.header)
        text = f'[color={color}] {self.header} [/color]'
        box.add(text, MenuAlignement.CENTER)
        render_order += 1
        menu_contents.append(box)
        mutable_y += 5

        available_options = list()
        available_options.append(f'{Texts.get_text("NEW_GAME")}')
        available_options.append(f'{Texts.get_text("LOAD_GAME")}')
        available_options.append(f'{Texts.get_text("OPTIONS_MENU")}')
        available_options.append(f'{Texts.get_text("QUIT")}')

        # REFACTO: TODO: modifier get_x_for_center_text avec len(text) au lieu de text directement.
        large_width = 0
        large_option_len = ''
        for option in available_options:
            if len(option) > large_width:
                large_width = len(option)
                large_option_len = option
        center_x = self.get_x_for_center_text(self.window_x, self.window_end_x, large_option_len)

        box = BoxMenu(render_order)
        color = config.COLOR_MAIN_MENU_OPTIONS
        for option in available_options:
            text = f'[color={color}]({chr(self.letter_index)}) {option}'
            box.add(text, MenuAlignement.CENTER)
            self.letter_index += 1
            mutable_y += 1
        menu_contents.append(box)

        self.window_end_y = mutable_y
        self.menu_contents = menu_contents


class QuitGameMenu(Menu):
    def initialize(self):
        self.create_menu_content()
        self.render_menu()

    def create_menu_content(self):
        render_order = 1
        menu_contents = list()
        mutable_y = self.window_y + 1

        # HEADER
        color = config.COLOR_MAIN_MENU_TITLE
        text = f'[color={color}] {self.header} [/color]'
        box = BoxMenu(render_order, linebreak=2)
        render_order += 1
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)
        mutable_y += 5

        available_options = list()
        available_options.append(Texts.get_text("NO"))
        available_options.append(Texts.get_text("YES"))

        # REFACTO: TODO: modifier get_x_for_center_text avec len(text) au lieu de text directement.
        # duplicate MainMenu - fonction Menu pour display des options? Utilisable aussi dans Item?
        large_width = 0
        for option in available_options:
            if len(option) > large_width:
                large_width = len(option)

        color = config.COLOR_MAIN_MENU_OPTIONS
        box = BoxMenu(render_order, linebreak=2)
        render_order += 1
        for option in available_options:
            text = f'[color={color}]({chr(self.letter_index)}) {option}'
            box.add(text, MenuAlignement.CENTER)
            self.letter_index += 1
            mutable_y += 1
        menu_contents.append(box)

        # HOW TO QUIT?
        mutable_y += 5
        box = BoxMenu(render_order)
        render_order += 1
        text = f' {Texts.get_text("ESCAPE_TO_CANCEL")} '
        text = f'[color=darker yellow]{text}[/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        self.window_end_y = mutable_y
        self.menu_contents = menu_contents


class MainOptionsMenu(Menu):
    def initialize(self):
        self.create_menu_content()
        self.render_menu()

    def create_menu_content(self):
        render_order = 1
        menu_contents = list()
        mutable_y = self.window_y + 1
        mutable_x = self.window_x

        # HEADER
        box = BoxMenu(render_order=1, linebreak=3)
        render_order += 1
        color = config.COLOR_MAIN_MENU_TITLE
        center_start = self.get_x_for_center_text(self.window_x, self.window_end_x, self.header)
        text = f'[color={color}] {self.header} [/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)
        mutable_y += 5

        available_options = list()
        available_options.append(Texts.get_text("CHANGE_LANGUAGE"))
        available_options.append(Texts.get_text("CHANGE_GRAPHICS"))
        available_options.append(Texts.get_text("BACK_TO_MAIN_MENU"))

        # REFACTO: TODO: modifier get_x_for_center_text avec len(text) au lieu de text directement.
        # duplicate MainMenu - fonction Menu pour display des options? Utilisable aussi dans Item?
        large_width = 0
        for option in available_options:
            if len(option) > large_width:
                large_width = len(option)

        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        color = config.COLOR_MAIN_MENU_OPTIONS
        for option in available_options:
            text = f'[color={color}]({chr(self.letter_index)}) {option}'
            box.add(text, MenuAlignement.CENTER)
            self.letter_index += 1
            mutable_y += 1
        menu_contents.append(box)

        # HOW TO QUIT?
        mutable_y += 5
        box = BoxMenu(render_order)
        render_order += 1
        text = f' {Texts.get_text("PRESS_ESCAPE_TO_MAIN_MENU")} '
        text = f'[color=darker yellow]{text}[/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        self.window_end_y = mutable_y
        self.menu_contents = menu_contents


class VictoryMenu(Menu):
    def initialize(self):
        self.create_menu_content()
        self.render_menu()

    def create_menu_content(self):
        render_order = 1
        menu_contents = list()
        mutable_y = self.window_y + 1
        mutable_x = self.window_x

        # HEADER
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        color = config.COLOR_MAIN_MENU_TITLE
        text = f'[color={color}] {self.header} [/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)
        mutable_y += 5

        mutable_x += 2
        box = BoxMenu(render_order)
        render_order += 1
        color = config.COLOR_MENU_BASE
        text = Texts.get_text("YOU_ESCAPE_DUNGEON")
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        menu_contents.append(box)

        # HOW TO QUIT?
        mutable_y += 5
        box = BoxMenu(render_order, linebreak=0)
        render_order += 1
        text = f' {Texts.get_text("PRESS_ESCAPE_TO_MAIN_MENU")} '
        text = f'[color=darker yellow]{text}[/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        self.window_end_y = mutable_y
        self.menu_contents = menu_contents


class GameOverMenu(Menu):
    def initialize(self):
        self.create_menu_content()
        self.render_menu()

    def create_menu_content(self):
        render_order = 1
        menu_contents = list()
        mutable_y = self.window_y + 1
        mutable_x = self.window_x

        # HEADER
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        color = config.COLOR_MAIN_MENU_TITLE
        text = f'[color={color}] {self.header} [/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)
        mutable_y += 5

        terminal.color(config.COLOR_MENU_BASE)
        logs = World.fetch('logs')
        print(f'menu: logs are {logs}')
        mutable_x += 5
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        count = 0
        for log in logs:
            if count < config.LOG_LIMIT_DEATH_SCREEN:
                box.add(log, MenuAlignement.CENTER)
                mutable_y += 1
                count += 1
        menu_contents.append(box)

        # HOW TO QUIT?
        mutable_y += 5
        box = BoxMenu(render_order, linebreak=0)
        render_order += 1
        text = f' {Texts.get_text("PRESS_ESCAPE_TO_MAIN_MENU")} '
        text = f'[color=darker yellow]{text}[/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        self.window_end_y = mutable_y
        self.menu_contents = menu_contents


class CharacterMenu(Menu):
    def initialize(self):
        self.create_menu_content()
        self.render_menu()

    def create_menu_content(self):
        # header = Texts.get_text('CHARACTER_SHEET_HEADER')
        render_order = 1
        menu_contents = list()
        player = World.fetch('player')
        player_attributes = World.get_entity_component(player, AttributesComponent)
        player_pools = World.get_entity_component(player, Pools)
        player_skills = World.get_entity_component(player, SkillsComponent)

        # variables
        mutable_y = self.window_y + 1
        mutable_y_right = self.window_y + 1

        # header
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        header = f'[color={config.COLOR_SYS_MSG}] {self.header} [/color]'
        box.add(header, MenuAlignement.CENTER)
        menu_contents.append(box)
        mutable_y += 3
        mutable_y_right += 3

        # CENTER TOP
        # level
        color = config.COLOR_MENU_BASE
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        text = Texts.get_text('CHARACTER_SHEET_CONTENT_LEVEL').format(player_pools.level)
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)

        mutable_y += 1
        mutable_y_right += 1

        text = Texts.get_text('CHARACTER_SHEET_CONTENT_XP').format(player_pools.xp,
                                                                    xp_for_next_level(player_pools.level))
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        mutable_y += 5
        mutable_y_right += 5
        menu_contents.append(box)

        # LEFT
        # attributes
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        color = config.COLOR_MENU_SUBTITLE_BASE
        text = Texts.get_text('CHARACTER_SHEET_CONTENT_ATTRIBUTES')
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        mutable_y += 2

        color = config.COLOR_MENU_BASE
        text = Texts.get_text('CHARACTER_SHEET_CONTENT_MIGHT').format(player_attributes.might)
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        mutable_y += 1

        text = Texts.get_text('CHARACTER_SHEET_CONTENT_BODY').format(player_attributes.body)
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        mutable_y += 1

        text = Texts.get_text('CHARACTER_SHEET_CONTENT_QUICKNESS').format(player_attributes.quickness)
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        mutable_y += 1

        text = Texts.get_text('CHARACTER_SHEET_CONTENT_WITS').format(player_attributes.wits)
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        mutable_y += 1
        menu_contents.append(box)

        # RIGHT
        # skills
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        color = config.COLOR_MENU_SUBTITLE_BASE
        text = Texts.get_text('CHARACTER_SHEET_CONTENT_SKILLS')
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        mutable_y_right += 2

        color = config.COLOR_MENU_BASE
        for skill in player_skills.skills:
            text = Texts.get_text(f'{skill}').format(player_skills.skills[skill])
            box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
            mutable_y_right += 1
        menu_contents.append(box)

        # BOTTOM: Equipped?
        if mutable_y_right > mutable_y:
            mutable_y = mutable_y_right
        mutable_y += 5

        # HOW TO QUIT?
        box = BoxMenu(render_order, linebreak=0)
        render_order += 1
        text = f' {Texts.get_text("ESCAPE_TO_CANCEL")} '
        text = f'[color=darker yellow]{text}[/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        self.window_end_y = mutable_y
        self.menu_contents = menu_contents


class InventoryMenu(Menu):
    def __init__(self, header):
        super().__init__(header)
        self.selected_item = None

    def initialize(self):
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

    def create_menu_content(self, decorated_names_list):
        print(f'inventory: create menu content')
        # content = (x, y, text)
        menu_contents = list()
        render_order = 1

        # variables
        mutable_y = self.window_y
        mutable_y_right = self.window_y

        # header
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        header = f'[color={config.COLOR_SYS_MSG}] {self.header} [/color]'  # On ajoute la couleur après le len()
        box.add(header, MenuAlignement.CENTER)
        menu_contents.append(box)
        mutable_y += 3
        mutable_y_right += 3

        # selected item
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        if self.selected_item:
            selected_content = Texts.get_text(get_item_display_name(self.selected_item))
        else:
            selected_content = Texts.get_text('INVENTORY_USAGE_EXPLANATION')
        selected_content = f'[color={config.COLOR_INFO_INVENTORY_SELECTED_ITEM}] {selected_content} [/color]'
        box.add(selected_content, MenuAlignement.CENTER)
        menu_contents.append(box)
        mutable_y += 3
        mutable_y_right += 3

        # left: item list.
        box = BoxMenu(render_order, linebreak=2)
        render_order += 1
        if not decorated_names_list:
            box.add(Texts.get_text('NO_ITEM_INVENTORY'), MenuAlignement.CENTER)
        for decorated_name in decorated_names_list:
            box.add(decorated_name, MenuAlignement.CENTER)
            mutable_y += 1
        menu_contents.append(box)

        # right: description
        box = BoxMenu(render_order)
        render_order += 1
        if self.selected_item:
            item_description_width_total = (self.window_end_x - self.window_x) // 2

            info_title = f'[color={config.COLOR_SYS_MSG}]{Texts.get_text("ITEM_INFO")}[/color]'
            box.add(info_title, MenuAlignement.CENTER)
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
                    box.add(f'[color={color}]{line}[/color]', MenuAlignement.CENTER)
                    mutable_y_right += 1
            mutable_y_right += 2

            # Some infos can be displayed, even if obfuscate
            color = config.COLOR_INFO_ATTRIBUTE_INVENTORY_MENU
            item_attribute_list = self.get_item_description(self.selected_item, obfuscate)
            for item_attribute in item_attribute_list:
                box.add(f'[color={color}]{item_attribute}[/color]', MenuAlignement.CENTER)
                mutable_y_right += 1
            menu_contents.append(box)

            # bottom: options if any.
            mutable_y = max(mutable_y, mutable_y_right)
            mutable_y += 3
            box = BoxMenu(render_order, linebreak=3)
            render_order += 1

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
                    box.add(f'[color={config.COLOR_INVENTORY_OPTION}]{option}[/color]',
                            MenuAlignement.CENTER)
                    mutable_x += large_width
                    if mutable_x + large_width >= self.window_end_x:
                        mutable_x = self.window_x + 2   # margin
                        mutable_y += 1
                menu_contents.append(box)
        mutable_y += 3

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

        self.window_end_y = mutable_y
        self.menu_contents = menu_contents

    def get_decorated_names_list(self, items_to_display, equipped):
        item_list_max_width = (self.window_end_x - self.window_x) // 2
        decorated_names_list = list()
        for item in items_to_display:
            item_name, equipped_info = self.reduce_item_option(item_list_max_width, item, equipped)
            # on ajoute la couleur de l'item + letter_index si pas d'items selectionnés
            if self.selected_item:
                if item == self.selected_item:
                    color = config.COLOR_INFO_SELECTED_ITEM_IN_INVENTORY
                else:
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

