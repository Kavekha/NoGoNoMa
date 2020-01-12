class WantsToDropComponent:
    def __init__(self, item_to_drop_id):
        self.item = item_to_drop_id


class WantsToMeleeComponent:
    def __init__(self, target):
        self.target = target


class WantsToPickUpComponent:
    def __init__(self, collector, item_to_pickup):
        self.collected_by = collector
        self.item = item_to_pickup


class WantsToUseComponent:
    def __init__(self, item_id, target=None):
        self.item = item_id
        self.target = target


class WantsToRemoveItemComponent:
    def __init__(self, item_id):
        self.item = item_id
