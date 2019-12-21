import config


class RawsItem:
    def __init__(self):
        self.name = None
        self.renderable = {}    # {'glyph': None, 'fg': None, 'order': None, 'sprite': None}
        self.consumable = {}    # {'effects': {'provides_healing': None,'damage': None,'ranged': None,
        # 'area_of_effect': None,'confusion': None}}
        self.weapon = {}    # {'range': None,'attribute': None, "min_dmg":None, "max_dmg":None, hit_bonus:None}
        self.wearable = {}    # {'slot': None, 'armor':None}
        self.magic = {}     # {'class': None, 'naming':None}


class RawsMob:
    def __init__(self):
        self.name = None
        self.renderable = None
        self.blocks_tile = True
        self.vision_range = 5
        self.attributes = {
            'might': 1,
            'body': 1,
            'quickness': 1,
            'wits': 1
        }
        self.skills = {}
        self.lvl = 1
        self.natural = None # {'armor':0, 'attacks':[ RefToIndexAttacks]


class RawsSpawnTable:
    def __init__(self):
        self.spawn_infos = {}   # {'name':{weight:0, min_depth:0, max_depth:0, add_map_depth_to_weight:False}

