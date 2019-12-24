import copy

from map_builders.map_model import Gmap
from gmap.spawner import spawn_entity
import config


class MapBuilder:
    def __init__(self, depth):
        self.map = Gmap(depth)
        self.starting_position = (0, 0)
        self.depth = depth
        self.history = list()
        self.map.create_fov_map()
        self.spawn_list = list()

    def reset(self):
        self.history = list()

    def get_spawn_list(self):
        return self.spawn_list

    def get_snapshot_history(self):
        return self.history

    def take_snapshot(self):
        if config.SHOW_MAPGEN_VISUALIZER:
            snapshot = copy.deepcopy(self.map)
            snapshot.revealed_tiles = [True] * (snapshot.height * snapshot.width)
            snapshot.visible_tiles = [True] * (snapshot.height * snapshot.width)
            self.history.append(snapshot)

    def build_map(self):
        self.build()
        self.spawn_entities()
        self.map.populate_blocked()
        self.map.create_fov_map()

    def spawn_entities(self):
        for spawn in self.spawn_list:
            spawn_entity(spawn[1], spawn[0], self.map)

    def get_map(self):
        return self.map

    def get_starting_position(self):
        return self.starting_position

    def build(self):
        raise NotImplementedError


class Rect:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    def intersect(self, other):
        if self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1:
            return True
        return False

    def center(self):
        return (self.x1 + self.x2)//2, (self.y1 + self.y2) // 2
