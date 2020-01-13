from bearlibterminal import terminal

from enum import Enum

from ui_system.render_menus import draw_background
from ui_system.render_functions import print_shadow
from world import World
from components.character_components import AttributesComponent
from components.pools_component import Pools
from components.skills_component import SkillsComponent
from player_systems.game_system import xp_for_next_level
from ui_system.ui_enums import Layers
from ui_system.text_functions import remove_color_tag
import config
from texts import Texts


class MenuAlignement(Enum):
    CENTER = 0
    LEFT = 1
    RIGHT = 2


class MenuPlacement(Enum):
    TOP = 0
    CENTER = 1
    BOTTOM = 2



class BoxMenu:
    def __init__(self, render_order=100, linebreak=0, margin=1):
        self.content = list()
        self.render_order = render_order
        self.linebreak = linebreak
        self.margin = margin

    def get_height(self):
        height = -1
        for _content in self.content:
            height += 1
        return height

    def get_total_height(self):
        # with line break
        height = 0
        for _content in self.content:
            height += 1
        height += self.linebreak
        height += self.margin
        return height

    def get_total_width(self):
        width = 0
        for content, _alignement in self.content:
            no_color_content = remove_color_tag(content)
            if len(no_color_content) > width:
                width = len(no_color_content)
        return width

    def add(self, text, alignement):
        cropped_text = self.crop_text(text)
        if type(cropped_text) == list:
            # c'est un groupe de lignes
            print(f'cropped text is line : {cropped_text}')
            for cropped_line in cropped_text:
                self.content.append((cropped_line, alignement))
        else:
            self.content.append((text, alignement))

    def get_center_point(self, width, len_text):
        center_x = (width - len_text) // 2
        return center_x

    def crop_text(self, text):
        width = config.MAX_MENU_SIZE_WIDTH
        # on perds la couleur
        no_color_content = remove_color_tag(text)
        if len(no_color_content) > width:
            words = no_color_content.split()
            new_content = list()
            line = ""
            while words:
                if len(line) < width:
                    # print(f'line is {line}, len {len(line)} vs width {width}')
                    to_add = words[0]
                    # print(f'to add {to_add}')
                    line += to_add + ' '
                    words.remove(to_add)
                    # print(f'after removing add : {words}')
                else:
                    new_content.append(f'[color={config.COLOR_MENU_BASE}]{line}[/color]')
                    line = ''
            if line:
                new_content.append(f'[color={config.COLOR_MENU_BASE}]{line}[/color]')
            return new_content
        else:
            return text

    def paste_on_window(self, x, y, width):
        mut_y = y
        max_y = self.get_height()

        previous_color = terminal.color(terminal.TK_COLOR)
        draw_background(x - self.margin, y - self.margin,
                        width + x + (2 * self.margin), y + max_y + self.margin,
                        'gray', bordure=False)
        terminal.color(previous_color)
        best_cx = 0
        for content, alignement in self.content:
            if alignement == MenuAlignement.CENTER:
                content_without_color = remove_color_tag(content)
                cx = self.get_center_point(width, len(content_without_color))
                if not best_cx:
                    best_cx = cx
                else:
                    if cx < best_cx:
                        best_cx = cx

        for content, alignement in self.content:
            print(f'content is {content} with {best_cx + x}, mut_y {mut_y}')
            print_shadow(best_cx + x, mut_y, content)
            mut_y += 1


class Menu:
    def __init__(self, header):
        self.header = header
        self.letter_index = ord('a')
        self.menu_contents = list()

    def menu_placement(self, width, height):
        screen_width = config.SCREEN_WIDTH
        screen_height = config.SCREEN_HEIGHT
        x1 = (screen_width - width) // 2
        y1 = (screen_height - height) // 2
        return x1, y1

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
        print(f'Menu: Render menu: i am {self}')
        terminal.layer(Layers.MENU.value)

        window_width = 0
        window_height = 0
        for content in self.menu_contents:
            content_width = content.get_total_width()
            if content_width > window_width:
                window_width = content_width
            window_height += content.get_total_height()
        x1, y1 = self.menu_placement(window_width, window_height)

        draw_background(x1 - 1, y1 - 1, x1 + window_width + 2, y1 + window_height + 1, color='gray')
        print(f'menu background : {x1, y1, x1 + window_width, y1 + window_height}')
        self.menu_contents = sorted(self.menu_contents, key=lambda cont: cont.render_order)
        for content in self.menu_contents:
            print(f'render menu: content {content}: paste on window {x1, y1}')
            y1 += content.margin
            content.paste_on_window(x1, y1, window_width)
            y1 += content.get_height()
            y1 += content.linebreak
            y1 += content.margin

        terminal.refresh()

    def get_x_for_center_text(self, x, width, text):
        raise NotImplementedError


class MainMenu(Menu):
    def initialize(self):
        self.create_content()
        self.render_menu()

    def create_content(self):
        menu_contents = list()
        render_order = 1

        # HEADER
        box = BoxMenu(render_order, linebreak=5, margin=1)
        color = config.COLOR_MAIN_MENU_TITLE
        text = f'[color={color}] {self.header} [/color]'
        box.add(text, MenuAlignement.CENTER)
        render_order += 1
        menu_contents.append(box)

        available_options = list()
        available_options.append(f'{Texts.get_text("NEW_GAME")}')
        available_options.append(f'{Texts.get_text("LOAD_GAME")}')
        available_options.append(f'{Texts.get_text("OPTIONS_MENU")}')
        available_options.append(f'{Texts.get_text("QUIT")}')

        # REFACTO: TODO: modifier get_x_for_center_text avec len(text) au lieu de text directement.
        large_width = 0
        for option in available_options:
            if len(option) > large_width:
                large_width = len(option)

        box = BoxMenu(render_order, margin=1)
        color = config.COLOR_MAIN_MENU_OPTIONS
        for option in available_options:
            text = f'[color={color}]({chr(self.letter_index)}) {option}'
            box.add(text, MenuAlignement.CENTER)
            self.letter_index += 1
        menu_contents.append(box)

        self.menu_contents = menu_contents


class QuitGameMenu(Menu):
    def initialize(self):
        self.create_menu_content()
        self.render_menu()

    def create_menu_content(self):
        render_order = 1
        menu_contents = list()

        # HEADER
        color = config.COLOR_MAIN_MENU_TITLE
        text = f'[color={color}] {self.header} [/color]'
        box = BoxMenu(render_order, linebreak=2, margin=1)
        render_order += 1
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        available_options = list()
        available_options.append(Texts.get_text("NO"))
        available_options.append(Texts.get_text("YES"))

        color = config.COLOR_MAIN_MENU_OPTIONS
        box = BoxMenu(render_order, linebreak=2, margin=1)
        render_order += 1
        for option in available_options:
            text = f'[color={color}]({chr(self.letter_index)}) {option}'
            box.add(text, MenuAlignement.CENTER)
            self.letter_index += 1
        menu_contents.append(box)

        # HOW TO QUIT?
        box = BoxMenu(render_order, margin=1)
        render_order += 1
        text = f' {Texts.get_text("ESCAPE_TO_CANCEL")} '
        text = f'[color=darker yellow]{text}[/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        self.menu_contents = menu_contents


class MainOptionsMenu(Menu):
    def initialize(self):
        self.create_menu_content()
        self.render_menu()

    def create_menu_content(self):
        render_order = 1
        menu_contents = list()

        # HEADER
        box = BoxMenu(render_order=1, linebreak=3)
        render_order += 1
        color = config.COLOR_MAIN_MENU_TITLE
        text = f'[color={color}] {self.header} [/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        available_options = list()
        available_options.append(Texts.get_text("CHANGE_LANGUAGE"))
        available_options.append(Texts.get_text("CHANGE_GRAPHICS"))
        available_options.append(Texts.get_text("BACK_TO_MAIN_MENU"))

        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        color = config.COLOR_MAIN_MENU_OPTIONS
        for option in available_options:
            text = f'[color={color}]({chr(self.letter_index)}) {option}'
            box.add(text, MenuAlignement.CENTER)
            self.letter_index += 1
        menu_contents.append(box)

        # HOW TO QUIT?
        box = BoxMenu(render_order)
        render_order += 1
        text = f' {Texts.get_text("PRESS_ESCAPE_TO_MAIN_MENU")} '
        text = f'[color=darker yellow]{text}[/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        self.menu_contents = menu_contents


class VictoryMenu(Menu):
    def initialize(self):
        self.create_menu_content()
        self.render_menu()

    def create_menu_content(self):
        render_order = 1
        menu_contents = list()

        # HEADER
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        color = config.COLOR_MAIN_MENU_TITLE
        text = f'[color={color}] {self.header} [/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        box = BoxMenu(render_order, linebreak=2)
        render_order += 1
        color = config.COLOR_MENU_BASE
        text = Texts.get_text("YOU_ESCAPE_DUNGEON")
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        menu_contents.append(box)

        # HOW TO QUIT?
        box = BoxMenu(render_order, linebreak=0)
        render_order += 1
        text = f' {Texts.get_text("PRESS_ESCAPE_TO_MAIN_MENU")} '
        text = f'[color=darker yellow]{text}[/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        self.menu_contents = menu_contents
        print('victory menu content is : ')
        for content in self.menu_contents:
            print(f'{content.content}')


class GameOverMenu(Menu):
    def initialize(self):
        self.create_menu_content()
        self.render_menu()

    def create_menu_content(self):
        render_order = 1
        menu_contents = list()

        # HEADER
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        color = config.COLOR_MAIN_MENU_TITLE
        text = f'[color={color}] {self.header} [/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        terminal.color(config.COLOR_MENU_BASE)
        logs = World.fetch('logs')
        print(f'menu: logs are {logs}')
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        count = 0
        for log in logs:
            if count < config.LOG_LIMIT_DEATH_SCREEN:
                box.add(log, MenuAlignement.CENTER)
                count += 1
        menu_contents.append(box)

        # HOW TO QUIT?
        box = BoxMenu(render_order, linebreak=0)
        render_order += 1
        text = f' {Texts.get_text("PRESS_ESCAPE_TO_MAIN_MENU")} '
        text = f'[color=darker yellow]{text}[/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

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

        # header
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        header = f'[color={config.COLOR_SYS_MSG}] {self.header} [/color]'
        box.add(header, MenuAlignement.CENTER)
        menu_contents.append(box)

        # CENTER TOP
        # level
        color = config.COLOR_MENU_BASE
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        text = Texts.get_text('CHARACTER_SHEET_CONTENT_LEVEL').format(player_pools.level)
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)

        text = Texts.get_text('CHARACTER_SHEET_CONTENT_XP').format(player_pools.xp,
                                                                    xp_for_next_level(player_pools.level))
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        menu_contents.append(box)

        # LEFT
        # attributes
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        color = config.COLOR_MENU_SUBTITLE_BASE
        text = Texts.get_text('CHARACTER_SHEET_CONTENT_ATTRIBUTES')
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)

        color = config.COLOR_MENU_BASE
        text = Texts.get_text('CHARACTER_SHEET_CONTENT_MIGHT').format(player_attributes.might)
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)

        text = Texts.get_text('CHARACTER_SHEET_CONTENT_BODY').format(player_attributes.body)
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)

        text = Texts.get_text('CHARACTER_SHEET_CONTENT_QUICKNESS').format(player_attributes.quickness)
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)

        text = Texts.get_text('CHARACTER_SHEET_CONTENT_WITS').format(player_attributes.wits)
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        menu_contents.append(box)

        # RIGHT
        # skills
        box = BoxMenu(render_order, linebreak=3)
        render_order += 1
        color = config.COLOR_MENU_SUBTITLE_BASE
        text = Texts.get_text('CHARACTER_SHEET_CONTENT_SKILLS')
        box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)

        color = config.COLOR_MENU_BASE
        for skill in player_skills.skills:
            text = Texts.get_text(f'{skill}') + f': {player_skills.skills[skill]}'
            box.add(f'[color={color}]{text}[/color]', MenuAlignement.CENTER)
        menu_contents.append(box)

        # BOTTOM: Equipped?

        # HOW TO QUIT?
        box = BoxMenu(render_order, linebreak=0)
        render_order += 1
        text = f' {Texts.get_text("ESCAPE_TO_CANCEL")} '
        text = f'[color=darker yellow]{text}[/color]'
        box.add(text, MenuAlignement.CENTER)
        menu_contents.append(box)

        self.menu_contents = menu_contents
