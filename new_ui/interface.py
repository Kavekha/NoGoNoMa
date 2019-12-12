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

    def __init__(self, mode=GraphicalModes.TILES):
        Interface.change_graphical_mode(mode)

    @staticmethod
    def change_graphical_mode(mode):
        print(f'-> Mode change requested with {mode}')
        if mode not in GraphicalModes:
            print(f'I am not graphical mode, stupid')
            return
        if mode == GraphicalModes.TILES:
            print(f'> Please load assets')
            Interface.load_graphical_assets()
        else:
            print(f'> Mode {mode} was not TILES')
        Interface.mode = mode

    @staticmethod
    def load_graphical_assets():
        print(f'----- ASSETS LOADING ------')
        for path in tilesets.SYSTEM:
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
        terminal.set(options)
        Interface.path_to_code.update({real_path: Interface.current_code})
        Interface.current_code += 1
