import pygame

from .data import Blittable
from .maths import Vector2
from pygame import Surface

class FontManager(Blittable):
    def __init__(self):
        self._current_string = None
        self._current_render_cache = None
        self._should_render = True

    def get_string_render(self, string):
        raise NotImplementedError

    def _font_draw_to(self, other_surface: Surface, pos: Vector2):
        raise NotImplementedError

    def update_string(self, string):
        if string != self._current_string:
            self._should_render = True
        self._current_string = string

    def draw_to(self, other_surface: Surface, pos: Vector2):
        if self._should_render:
            if self._current_string is None:
                raise ValueError("attempted to draw font to surface without setting it first.")
            else:
                self._current_rendered_string = self._current_string
                self._current_render_cache = self.get_string_render(self._current_rendered_string)

        self._font_draw_to(other_surface, pos)

class RegularFontManager(FontManager):
    def __init__(self, color, name, size, anti_alias=True):
        super().__init__()
        self._color = color
        self._font = pygame.font.SysFont(name, size)
        self._anti_alias = anti_alias

    def get_string_render(self, string):
        return self._font.render(string, self._anti_alias, self._color)

    def _font_draw_to(self, other_surface, pos):
        other_surface.blit(self._current_render_cache, tuple(pos))

class SpriteFontManager(FontManager):
    def __init__(self, font_dict, padding_px):
        super().__init__()
        self.font_dict = font_dict
        self.padding_px = padding_px

    def get_string_render(self, string):
        result = []

        current_x_offset = 0
        for char in string:
            r_char = self.font_dict[char]
            result.append((
                r_char,
                current_x_offset,
            ))
            current_x_offset += self.padding_px + r_char.size.x

        return result

    def _font_draw_to(self, other_surface, pos):
        for (render, offset) in self._current_render_cache:
            other_surface.blit(
                render.inner,
                (pos[0] + offset, pos[1])
            )
