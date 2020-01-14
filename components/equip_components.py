class EquippedComponent:
    def __init__(self, owner, equipment_slot):
        self.owner = owner
        self.slot = equipment_slot


class EquippableComponent:
    def __init__(self, equipment_slot):
        self.slot = equipment_slot


class EquipmentChangedComponent:
    pass
