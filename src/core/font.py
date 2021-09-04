import pygame
import abc
from pygame import Surface
from typing import List, Tuple, Optional, cast, Dict, Any

from .data import Blittable, PygameSurface
from .maths import Vector2

RenderInfo = Tuple[PygameSurface, Vector2]

class FontManager(Blittable):
    def __init__(self, initial_string: str):
        super().__init__()
        self._current_string = initial_string
        self._current_rendered_string: Optional[str] = None
        self._current_render_cache: Optional[List[RenderInfo]] = None
        self._should_render = True

    @abc.abstractmethod
    def get_width(self) -> int:
        """Get the current string's width."""

    @abc.abstractmethod
    def get_height(self) -> int:
        """Get the current string's height."""

    @property
    def size(self) -> Vector2:
        """Get the current string's width and height.

        If not overrided, is equivalent to calling the `get_width` and `get_height` methods directly.

        Overriding is recommended for when there is a more lightweight way of calculating both width and height at the same time.
        """
        return Vector2(self.get_width(), self.get_height())

    def get_render(self) -> List[RenderInfo]:
        """Analyze the current string and returns a list of surfaces (with positions and their sizes).

        If not overrided, uses `get_render_for_string` internally, and, therefore, depends on its implementation.
        """
        if self._should_render or self._current_render_cache is None:
            self._current_rendered_string = self._current_string
            self._current_render_cache = self.get_render_for_string(self._current_rendered_string)
            self._should_render = True

        return self._current_render_cache

    @abc.abstractmethod
    def get_render_for_string(self, string: str) -> List[RenderInfo]:
        """Analyze some other string (which is not necessarily the current one) and, using this font manager's state, renders it."""

    def update_string(self, string: str) -> None:
        if string != self._current_string:
            self._should_render = True
        self._current_string = string

    def draw_to(self, surface: Surface, pos: Vector2) -> None:
        if self._should_render:
            self.get_render()

        assert self._current_render_cache is not None
        for (render, offset) in self._current_render_cache:
            surface.blit(render.inner, pos.map_with_other(offset, lambda a, b: a + b).to_tuple())

class RegularFontManager(FontManager):
    def __init__(self, color, font_name: str, font_size: int, initial_string: str, anti_alias: bool = True):
        super().__init__(initial_string=initial_string)
        self._color = color
        self._font = pygame.font.SysFont(font_name, font_size)
        self._anti_alias = anti_alias

    def get_width(self) -> int:
        return self._font.size(self._current_string)[0]

    def get_height(self) -> int:
        return self._font.size(self._current_string)[1]

    @property
    def size(self) -> Vector2:
        return Vector2.from_tuple(self._font.size(self._current_string))

    def get_render_for_string(self, string: str) -> List[RenderInfo]:
        return [(
            PygameSurface(cast(pygame.Surface, self._font.render(string, self._anti_alias, self._color))),
            Vector2(0, 0),
        )]

class SpriteFontManager(FontManager):
    def __init__(
        self,
        font_dict: Dict[str, Any],
        padding_px: int,
        initial_string: str,
        scale: float = 1.0,
    ):
        super().__init__(initial_string=initial_string)
        self.font_dict = font_dict
        self.padding_px = padding_px
        self.scale = scale

    @property
    def size(self) -> Vector2:
        renders = self.get_render()

        _, start_pos = renders[0]
        end_surf, end_pos = renders[-1]

        width = (end_pos.x + end_surf.size.x) - start_pos.x
        height = max(map(lambda render: render[0].size.y, renders))

        return Vector2(width, height)

    def get_render_for_string(self, string: str) -> List[RenderInfo]:
        result = []

        current_x_offset = 0
        for char in string:
            r_char = self.font_dict[char].scaled(
                Vector2(self.scale, self.scale)
            )

            y_offset = -r_char.size.y
            result.append((r_char, Vector2(current_x_offset, y_offset)))
            current_x_offset += self.padding_px * self.scale + r_char.size.x

        return result
