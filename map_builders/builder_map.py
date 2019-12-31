from copy import deepcopy

from map_builders.map_model import Gmap
from gmap.spawner import spawn_entity
import config


class InitialMapBuilder:
    def build_map(self, build_data):
        raise NotImplementedError


class MetaMapbuilder:
    def __init__(self, *args):
        self.args = args
        print(f'args is {self.args}')

    def build_meta_map(self, build_data):
        raise NotImplementedError


class BuilderMap:
    def __init__(self, depth, width, height):
        self.spawn_list = list()
        self.map = Gmap(depth, width, height)
        self.starting_position = (0, 0)
        self.rooms = None
        self.corridors = None
        self.history = list()

    def take_snapshot(self):
        if config.SHOW_MAPGEN_VISUALIZER:
            snapshot = deepcopy(self.map)
            snapshot.revealed_tiles = [True] * (snapshot.height * snapshot.width)
            snapshot.visible_tiles = [True] * (snapshot.height * snapshot.width)
            self.history.append(snapshot)


class BuilderChain:
    def __init__(self, depth, width, height):
        self.starter = None
        self.builders = list()
        self.build_data = BuilderMap(depth, width, height)

    def start_with(self, initial_map_builder):
        if self.starter:
            print(f'BuilderChain has already a starter builder. Cant add a new one : {initial_map_builder}')
            raise AssertionError
        else:
            self.starter = initial_map_builder

    def build_with(self, metabuilder):
        self.builders.append(metabuilder)

    def build_map(self):
        if not self.starter:
            print('Cant build map without a starter builder!')
            raise NotImplementedError
        print(f'build map from InitialMap : starter is {self.starter}')
        print(f'build map from initialmap : build data is {self.build_data}')
        self.starter.build_initial_map(self.build_data)

        for metabuilder in self.builders:
            print(f'playing : {metabuilder}, from {self.builders}')
            metabuilder.build_meta_map(self.build_data)

        # mandatory to work
        self.build_data.map.populate_blocked()
        self.build_data.map.create_fov_map()

    def spawn_entities(self):
        for spawn in self.build_data.spawn_list:
            spawn_entity(spawn[1], spawn[0], self.build_data.map)


