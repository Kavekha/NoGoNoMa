from ui_system.ui_enums import Layers


class RenderableComponent:
    def __init__(self, glyph, char_color, sprite='chars/morblin.png', render_order=Layers.UNKNOWN):
        self.glyph = glyph
        self.fg = char_color
        self.render_order = render_order
        self.sprite = sprite
