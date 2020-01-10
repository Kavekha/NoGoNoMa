class PositionComponent:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ApplyMoveComponent:
    def __init__(self, dest_idx):
        self.dest_idx = dest_idx


class EntityMovedComponent:
    pass
