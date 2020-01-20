def parse_particule(string):
    tokens = string.split(';')
    return {'glyph': tokens[0],
            'color': tokens[1],
            'sprite': tokens[2]}



