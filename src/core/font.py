from .render import BatchRender
from .maths import Vector2

class SpriteFont:
    def __init__(self, font_dict):
        assert isinstance(font_dict, dict)
        self.font_dict = font_dict

    def render_string(self, string):
        return [self.font_dict[c] for c in string]

class FontManager(BatchRender):
    def __init__(self, pos, sprite_font, padding_px):
        assert isinstance(sprite_font, SpriteFont)
        self.pos = Vector2(pos)
        self.sprite_font = sprite_font
        self.padding_px = int(padding_px)
        self.should_update = False

        self._string = ""

    def update_string(self, string):
        self._string = string

    def get_render(self):
        base_x, base_y = self.pos.into_tuple()

        ls = []
        current_x = base_x
        for char_surface in self.sprite_font.render_string(self._string):
            ls.append((char_surface, (current_x, base_y)))
            current_x += char_surface.size.x + self.padding_px

        return ls
