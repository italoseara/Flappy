import pygame

from .render import Render
from .data import Blittable, PygameSurface
from .maths import Vector2

class GameManager:
    def __init__(self, title: str, win_size: Vector2):
        self.title = title
        self._win_size = tuple(map(int, win_size.to_tuple()))

        self._screen = PygameSurface(pygame.display.set_mode(self._win_size, vsync=True))
        pygame.display.set_caption(self.title)

    def set_icon(self, icon):
        pygame.display.set_icon(icon.into_pygame())

    def fill_screen(self, color):
        self._screen.into_pygame().fill(color)

    def render(self, render: Render):
        render.draw_to(self._screen.into_pygame())

    def blit(self, blittable: Blittable, pos: Vector2):
        blittable.draw_to(self._screen.into_pygame(), pos)

    def render_rect(self, rect, line_color, line_size):
        pygame.draw.rect(self._screen.into_pygame(), line_color, rect, line_size)
