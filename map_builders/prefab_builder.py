from random import randint
from copy import deepcopy

from map_builders.map_builders import MapBuilder
from gmap.gmap_enums import TileType
from map_builders.builder_structs import HorizontalPlacement, VerticalPlacement, \
    TOTALY_NOT_A_TRAP, SILLY_SMILE_MAP, CHECKERBOARD_MAP
from map_builders.commons import return_most_distant_reachable_area
from gmap.spawner import spawn_entity

import config


class PrefabLevel:
    def __init__(self, template, width, height):
        self.template = template
        self.width = width
        self.height = height


class PrefabRoom:
    def __init__(self, template, width, height, first_depth, last_depth):
        self.template = template
        self.width = width
        self.height = height
        self.first_depth = first_depth
        self.last_depth = last_depth


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
        elif type(self.template) == PrefabLevel:  # Constant
            # self.template = PrefabLevel(LEVEL_MAP, 80, 42)
            self.load_ascii_map()
        elif type(self.template) == PrefabSection:  # Sectionnal
            self.apply_sectionnal()
        elif type(self.template) == PrefabRoom:  # Room Vault
            print(f'VAULT !')
            self.apply_room_vaults()
        else:
            print(f'This object is not valid as a template : {self.template} : {type(self.template)}')
            raise NotImplementedError

        self.map.revealed_tiles = [True] * (self.map.height * self.map.width)
        self.map.visible_tiles = [True] * (self.map.height * self.map.width)

        x, y = self.starting_position
        best_exit = return_most_distant_reachable_area(self.map, self.map.xy_idx(x, y))

        if best_exit:
            if self.depth != config.MAX_DEPTH:
                self.map.tiles[best_exit] = TileType.DOWN_STAIRS
            else:
                self.map.tiles[best_exit] = TileType.EXIT_PORTAL

    def apply_room_vaults(self):
        print('VAULT: apply room')
        x = y = 0
        self.apply_previous_iteration(x, y)

        vault_roll = randint(1, 6)
        if vault_roll < 4:
            return

        # placeholders
        master_vault_list = [PrefabRoom(TOTALY_NOT_A_TRAP, 5, 5, 0, 100),
                             PrefabRoom(SILLY_SMILE_MAP, 6, 6, 0, 100),
                             PrefabRoom(CHECKERBOARD_MAP, 6, 6, 0, 100)]

        print(f'VAULT : master vault list is {master_vault_list}')

        # looking for a valid available vault
        possible_vaults = list()
        for vault in master_vault_list:
            if vault.first_depth < self.map.depth < vault.last_depth:
                possible_vaults.append(vault)

        used_tiles = dict()  # to add the tiles we overlap with one room, so we dont add another on it.
        nb_vaults = randint(1, 3)
        for j in range(0, nb_vaults):
            if not possible_vaults:
                break
            if len(possible_vaults) == 1:
                vault_index = 0
            else:
                vault_index = randint(1, len(possible_vaults)) - 1
            vault = possible_vaults[vault_index]

            # looking for places to put the vault.
            vault_positions = list()
            idx = 0
            while True:
                x, y = self.map.index_to_point2d(idx)

                # in the map?
                if x > 1 and (x + vault.width) < self.map.width - 2 and y > 1 and (
                        y + vault.height) < self.map.height - 2:
                    possible = True
                    for vy in range(0, vault.height):
                        for vx in range(0, vault.width):
                            idx = self.map.xy_idx(vx + x, vy + y)
                            if self.map.tiles[idx] is not TileType.FLOOR:
                                possible = False
                            if used_tiles.get(idx):
                                possible = False

                    if possible:
                        vault_positions.append((x, y))

                idx += 1
                if idx >= len(self.map.tiles) - 1:
                    break

            # si des positions ont été trouvées
            if vault_positions:
                if len(vault_positions) == 1:
                    pos_index = 0
                else:
                    pos_index = randint(0, len(vault_positions)) - 1
                position = vault_positions[pos_index]
                chunk_x, chunk_y = position

                # char to map incoming
                string_vec = self.template.template
                string_vec = string_vec.replace('\n', '').replace('\r', '')

                i = 0
                for y in range(0, vault.height - 1):
                    for x in range(0, vault.width - 1):
                        idx = self.map.xy_idx(x + chunk_x, y + chunk_y)
                        self.char_to_map(string_vec[i], idx)
                        # print(f'string vec is {string_vec} and i - 1 is : {string_vec[i - 1]}')
                        used_tiles[idx] = True
                        i += 1
                self.take_snapshot()

                # remove spawn in spawn list where spawn in our vault
                spawn_list_to_keep = deepcopy(self.spawn_list)
                print(f'SPAWN LIST REMOVAL = {spawn_list_to_keep}')
                for i, (spawn_idx, spawn_name) in enumerate(self.spawn_list):
                    x, y = self.map.index_to_point2d(spawn_idx)
                    # if x and y in vault
                    if chunk_x < x < chunk_x + vault.width and chunk_y < y < chunk_y + vault.height:
                        spawn_list_to_keep.remove(self.spawn_list[i])
                        print(f'original: {self.spawn_list}')
                        print(f'copie: {spawn_list_to_keep}')

                self.spawn_list = spawn_list_to_keep

            self.take_snapshot()
            possible_vaults.remove(vault)

    def apply_previous_iteration(self, section_x, section_y):
        # build map
        prev_builder = self.previous_builder
        prev_builder.build_map()
        self.starting_position = prev_builder.get_starting_position()
        self.map = deepcopy(prev_builder.get_map())
        for entity in prev_builder.get_spawn_list():
            idx = entity[0]
            x, y = self.map.index_to_point2d(idx)
            if section_x > x > (section_x + self.template.width) and section_y > y > (section_y + self.template.height):
                self.spawn_list.append((idx, entity[1]))
        self.take_snapshot()

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

        self.apply_previous_iteration(chunk_x, chunk_y)

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
