import config


class ViewshedComponent:
    def __init__(self, visible_range=config.DEFAULT_VISIBILITY):
        self.visible_tiles = []
        self.visible_range = visible_range
        self.light_wall = True
        self.dirty = True