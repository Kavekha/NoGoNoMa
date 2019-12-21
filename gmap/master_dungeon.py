from data.load_raws import RawsMaster
from player_systems.game_system import make_scroll_name


class MasterDungeon:
    def __init__(self):
        self.maps = dict()
        self.identified_items = set()
        self.scroll_mappings = dict()

        for scroll in RawsMaster.get_scroll_tags():
            masked_name = make_scroll_name()
            self.scroll_mappings[scroll] = masked_name

    def store_map(self, depth, map):
        self.maps[depth] = map

    def get_map(self, depth):
        result = self.maps.get(depth)
        if result:
            return result
        return False


