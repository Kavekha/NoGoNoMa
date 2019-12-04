class RawsItem:
    def __init__(self):
        self.name = None
        self.renderable = {}    # {'glyph': None, 'fg': None, 'order': None}
        self.consumable = {}    # {'effects': {'provides_healing': None,'damage': None,'ranged': None,
        # 'area_of_effect': None,'confusion': None}}
        self.weapon = {}    # {'range': None,'power_bonus': None}
        self.shield = {}    # {'defense_bonus': None}


class RawsMob:
    def __init__(self):
        self.name = None
        self.renderable = None
        self.blocks_tile = True
        self.stats = {
            'max_hp': 1,
            'defense': 0,
            'power': 0
        }
        self.vision_range = 5


class RawsSpawnTable:
    def __init__(self):
        self.spawn_infos = {}   # {'name':{weight:0, min_depth:0, max_depth:0, add_map_depth_to_weight:False}

