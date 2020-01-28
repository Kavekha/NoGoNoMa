from components.name_components import NameComponent
from components.spell_components import SpellTemplate

def parse_particule(string):
    tokens = string.split(';')
    return {'glyph': tokens[0],
            'color': tokens[1],
            'sprite': tokens[2]}


def find_spell_entity(name):
    from world import World
    subjects = World.get_components(NameComponent, SpellTemplate)
    for entity, (spell_name, spell_template) in subjects:
        if name == spell_name.name:
            return entity
