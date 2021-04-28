# TODO: remake this API (probably using abc and dataclasses) and make it more readable

import pygame
import abc
from pygame import Surface
from typing import Any, List, Tuple

from .data import Blittable
from .maths import Vector2

class FontManager(Blittable):
    def __init__(self, initial_string: str):
        super().__init__()
        self._current_string = initial_string
        self._current_rendered_string = None
        self._current_render_cache = None
        self._should_render = True

    @abc.abstractmethod
    def get_width(self) -> int: ...

    @abc.abstractmethod
    def get_height(self) -> int: ...

    @abc.abstractmethod
    def get_string_render(self, string: str) -> List[Tuple[Surface, int, int]]: ...

    @abc.abstractmethod
    def _font_draw_to(self, surface: Surface, offset: Vector2) -> None: ...

    def update_string(self, string: str) -> None:
        if string != self._current_string:
            self._should_render = True
        self._current_string = string

    def draw_to(self, surface: Surface, pos: Vector2) -> None:
        if self._should_render:
            self._current_rendered_string = self._current_string
            self._current_render_cache = self.get_string_render(self._current_rendered_string)

        self._font_draw_to(surface, pos)

class RegularFontManager(FontManager):
    def __init__(self, color, font_name: int, font_size: float, initial_string: str, anti_alias: bool = True):
        super().__init__(initial_string=initial_string)
        self._color = color
        self._font = pygame.font.SysFont(font_name, font_size)
        self._anti_alias = anti_alias

    def get_string_render(self, string: str) -> Any:
        return self._font.render(string, self._anti_alias, self._color)

    def _font_draw_to(self, surface: Surface, offset: Vector2) -> None:
        other_surface.blit(self._current_render_cache, tuple(pos))

class SpriteFontManager(FontManager):
    def __init__(self, font_dict, padding_px: int, initial_string: str):
        super().__init__(initial_string=initial_string)
        self.font_dict = font_dict
        self.padding_px = padding_px

    def get_width(self, string: str) -> int:
        renders = self.get_string_render(string)

        (_, start_x, _) = renders[0]
        (_, end_x, char_width) = renders[-1]

        return (end_x + char_width) - start_x

    def get_string_render(self, string: str) -> List[Tuple[Surface, int, int]]:
        result = []

        current_x_offset = 0
        for char in string:
            r_char = self.font_dict[char]
            result.append((r_char, current_x_offset, r_char.size.x))
            current_x_offset += self.padding_px + r_char.size.x

        return result

    def _font_draw_to(self, surface: Surface, offset: Vector2) -> None:
        for (render, h_offset, _) in self._current_render_cache:
            surface.blit(render.inner, (offset[0] + h_offset, offset[1]))
