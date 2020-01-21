def parse_particule(string):
    tokens = string.split(';')
    return {'glyph': tokens[0],
            'color': tokens[1],
            'sprite': tokens[2]}


def find_spell_entity(name):
    print(f'find spell entity: spell name is {name}')
    from components.name_components import NameComponent
    from components.spell_components import SpellTemplate
    from world import World
    subjects = World.get_components(NameComponent, SpellTemplate)
    for entity, (spell_name, spell_template) in subjects:
        print(f'find spell entity: subjects : {entity}, {spell_name.name}, {spell_template}')
        if name == spell_name.name:
            return entity
