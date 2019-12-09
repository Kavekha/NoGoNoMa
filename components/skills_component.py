from enum import Enum


class Skills(Enum):
    MELEE = 0
    DEFENSE = 1


class SkillsComponent:
    def __init__(self):
        self.skills = {}
