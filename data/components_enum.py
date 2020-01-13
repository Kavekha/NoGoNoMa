from enum import Enum


class EquipmentSlots(Enum):
    MELEE = 0
    SHIELD = 1
    HELM = 2
    TORSO = 3
    GAUNTLET = 4


class WeaponAttributes(Enum):
    MIGHT = 0
    QUICKNESS = 1


class MagicItemClass(Enum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    EPIC = 3
    LEGENDARY = 4

