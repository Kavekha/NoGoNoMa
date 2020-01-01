from bearlibterminal import terminal

from enum import Enum
from data import tilesets
import config


class GraphicalModes(Enum):
    ASCII = 0
    TILES = 1


class Interface:
    path_to_code = {}
    current_code = 0xE000
    code_limit = 0xF8FF
    mode = None
    zoom = 2
    screen_width = config.SCREEN_WIDTH
    screen_height = config.SCREEN_HEIGHT
    list_of_tilesets = tilesets.SYSTEM + tilesets.CHARS + tilesets.MAP + tilesets.ITEMS + \
                       tilesets.PARTICULES + tilesets.PROPS

    def __init__(self, mode=GraphicalModes.TILES):
        print(f'interface INIT')
        Interface.change_graphical_mode(mode)

    @staticmethod
    def initialize():
        Interface.set_zoom(2)

    @staticmethod
    def change_graphical_mode(mode):
        print(f'-> Mode change requested with {mode}')
        if mode not in GraphicalModes:
            print(f'I am not graphical mode, stupid')
            return
        elif mode == GraphicalModes.TILES:
            print(f'> Please load assets')
            Interface.load_graphical_assets()
        elif mode == GraphicalModes.ASCII:
            Interface.set_zoom(1)
        else:
            print(f'> Mode {mode} was not TILES')
        Interface.mode = mode

    @staticmethod
    def load_graphical_assets():
        print(f'----- ASSETS LOADING ------')
        list_of_tilesets = tilesets.SYSTEM + tilesets.CHARS + tilesets.MAP + tilesets.ITEMS + \
                       tilesets.PARTICULES + tilesets.PROPS
        for path in list_of_tilesets:
            Interface.get_new_code_for_path(path)

    @staticmethod
    def get_code(path):
        real_path = '/'.join([config.TILE_DIR, path])
        if Interface.path_to_code.get(real_path):
            return Interface.path_to_code.get(real_path)
        else:
            print(f'no path for {path} in Tilesets')
            raise NotImplementedError

    @staticmethod
    def get_new_code_for_path(path):
        real_path = '/'.join([config.TILE_DIR, path])
        options = f'{Interface.current_code}:{real_path}'

        cell_width = terminal.state(terminal.TK_CELL_WIDTH)
        font_options = '{}: {}, resize={}x{}'.format(str(Interface.current_code), real_path,
                                                     str(cell_width * Interface.zoom), str(cell_width * Interface.zoom))

        if options:
            font_options += ', ' + options

        font_options += ', ' + 'resize-filter=nearest'

        terminal.set(options)
        Interface.path_to_code.update({real_path: Interface.current_code})
        Interface.current_code += 1
        return Interface.current_code - 1

    @staticmethod
    def set_zoom(zoom=2):
        if Interface.mode == GraphicalModes.ASCII:
            Interface.zoom = 1
        else:
            if 1 <= zoom <= 4:
                Interface.zoom = zoom
            elif zoom < 1:
                Interface.zoom = 1
            else:
                Interface.zoom = 4

        cell_width = terminal.state(terminal.TK_CELL_WIDTH)
        Interface.resize_tiles(cell_width * Interface.zoom)
        Interface.screen_width = config.SCREEN_WIDTH // Interface.zoom
        Interface.screen_height = config.SCREEN_HEIGHT // Interface.zoom

    @staticmethod
    def resize_tiles(resize):
        # Tous, sauf ceux interface
        list_of_tilesets = tilesets.CHARS + tilesets.MAP + tilesets.ITEMS + \
                           tilesets.PARTICULES + tilesets.PROPS
        for path in list_of_tilesets:
            real_path = '/'.join([config.TILE_DIR, path])
            code = Interface.path_to_code[real_path]
            Interface.set_tile(path, code, resize)

    @staticmethod
    def set_tile(path, code, resize, option='', icon=False):
        real_path = '/'.join([config.TILE_DIR, path])

        font_options = '{}: {}, resize={}x{}'.format(str(code), real_path,
                                                     str(resize), str(resize))

        if option:
            font_options += ', ' + option

        font_options += ', ' + 'resize-filter=nearest'

        terminal.set(font_options)

        if icon:
            path = 'icon/' + path
        Interface.path_to_code.update({path: code})
