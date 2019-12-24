from random import randint
from copy import deepcopy

from map_builders.map_builders import MapBuilder
from gmap.gmap_enums import TileType
from map_builders.builder_structs import LEVEL_MAP, HorizontalPlacement, VerticalPlacement, PrefabMode
from map_builders.commons import return_most_distant_reachable_area, generate_voronoi_spawn_points, paint
from gmap.spawner import spawn_entity

import config


class PrefabLevel:
    def __init__(self, template, width, height):
        self.template = template
        self.width = width
        self.height = height


class PrefabSection:
    def __init__(self, template, width, height, placement):
        self.template = template
        self.width = width
        self.height = height
        self.placement = placement


class PrefabBuilder(MapBuilder):
    def __init__(self, depth, template=None, previous_builder=None):
        super().__init__(depth)
        self.noise_areas = list()
        self.template = template
        self.previous_builder = previous_builder

    def spawn_entities(self):
        for spawn in self.spawn_list:
            spawn_entity(spawn[1], spawn[0], self.map)

    def build(self):
        if not self.template:
            print(f'no valid template given for Prefab')
            raise NotImplementedError
        elif type(self.template) == PrefabLevel:    # Constant
            # self.template = PrefabLevel(LEVEL_MAP, 80, 42)
            self.load_ascii_map()
        elif type(self.template) == PrefabSection:  # Sectionnal
            self.apply_sectionnal()
            print(f'no mode given')

        self.map.revealed_tiles = [True] * (self.map.height * self.map.width)
        self.map.visible_tiles = [True] * (self.map.height * self.map.width)

        x, y = self.starting_position
        best_exit = return_most_distant_reachable_area(self.map, self.map.xy_idx(x, y))

        if best_exit:
            if self.depth != config.MAX_DEPTH:
                self.map.tiles[best_exit] = TileType.DOWN_STAIRS
            else:
                self.map.tiles[best_exit] = TileType.EXIT_PORTAL

    def apply_sectionnal(self):
        # New section coords
        chunk_x = 0
        if type(self.template.placement[0]) is not HorizontalPlacement:
            print(f'placement should be a tuple, with Horizontal as first option')
            raise SyntaxError
        elif self.template.placement[0] == HorizontalPlacement.LEFT:
            chunk_x = 0
        elif self.template.placement[0] == HorizontalPlacement.CENTER:
            chunk_x = (self.map.width // 2) - (self.template.width // 2)
        elif self.template.placement[0] == HorizontalPlacement.RIGHT:
            chunk_x = (self.map.width - 1) - self.template.width

        chunk_y = 0
        if type(self.template.placement[1]) is not VerticalPlacement:
            print(f'placement should be a tuple, with Horizontal as first option')
            raise SyntaxError
        elif self.template.placement[1] == VerticalPlacement.TOP:
            chunk_y = 0
        elif self.template.placement[1] == VerticalPlacement.CENTER:
            chunk_y = (self.map.height // 2) - (self.template.height // 2)
        elif self.template.placement[1] == VerticalPlacement.BOTTOM:
            chunk_y = (self.map.height - 1) - self.template.height

        # build map
        prev_builder = self.previous_builder
        prev_builder.build_map()
        self.starting_position = prev_builder.get_starting_position()
        self.map = deepcopy(prev_builder.get_map())
        for entity in prev_builder.get_spawn_list():
            idx = entity[0]
            x, y = self.map.index_to_point2d(idx)
            if chunk_x > x > (chunk_x + self.template.width) and chunk_y > y > (chunk_y + self.template.height):
                self.spawn_list.append((idx, entity[1]))
        self.take_snapshot()

        string_vec = self.template.template
        string_vec = string_vec.replace('\n', '').replace('\r', '')

        print(f'sectionnal: template is : \n{self.template.template}')

        i = 0
        for y in range(0, self.template.height):
            for x in range(0, self.template.width):
                if x < self.map.width and y < self.map.height:
                    idx = self.map.xy_idx(x + chunk_x, y + chunk_y)
                    self.char_to_map(string_vec[i], idx)
                i += 1

        self.take_snapshot()

    def char_to_map(self, char, idx):
        if char == ' ':
            self.map.tiles[idx] = TileType.FLOOR
        elif char == '#':
            self.map.tiles[idx] = TileType.WALL
        elif char == '@':
            self.map.tiles[idx] = TileType.FLOOR
            self.starting_position = self.map.index_to_point2d(idx)
        elif char == '>':
            self.map.tiles[idx] = TileType.DOWN_STAIRS
        elif char == 'g':
            self.map.tiles[idx] = TileType.FLOOR
            self.spawn_list.append((idx, "MORBLIN"))
        elif char == 'o':
            self.map.tiles[idx] = TileType.FLOOR
            self.spawn_list.append((idx, "OOGLOTH"))
        elif char == '^':
            self.map.tiles[idx] = TileType.FLOOR
            self.spawn_list.append((idx, "TRAP"))
        elif char == '%':
            self.map.tiles[idx] = TileType.FLOOR
            self.spawn_list.append((idx, "DAGGER"))
        elif char == '!':
            self.map.tiles[idx] = TileType.FLOOR
            self.spawn_list.append((idx, "HEALTH_POTION"))
        else:
            if char == '\n' or char == '\r':
                self.map.tiles[idx] = TileType.EXIT_PORTAL
            else:
                print(f'Char {char} not implemented')
                raise NotImplementedError

    def load_ascii_map(self):
        string_vec = self.template.template
        string_vec = string_vec.replace('\n', '').replace('\r', '')

        i = 0
        for y in range(0, self.template.height):
            for x in range(0, self.template.width):
                if x < self.map.width and y < self.map.height:
                    idx = self.map.xy_idx(x, y)
                    self.char_to_map(string_vec[i], idx)
                i += 1
            if randint(1, 10) == 1:
                self.take_snapshot()
