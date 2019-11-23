from data.types import Layers


class RenderableComponent:
    def __init__(self, glyph, char_color, render_order=Layers.UNKNOWN):
        self.glyph = glyph
        self.fg = char_color
        self.render_order = render_order
