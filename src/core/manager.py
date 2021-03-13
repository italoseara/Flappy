import pygame

from .render import Render
from .data import Blittable
from .maths import Vector2

class GameManager:
    def __init__(self, title, win_size):
        self.title = title
        self.win_size = tuple(win_size)

        self._screen = pygame.display.set_mode(self.win_size)
        pygame.display.set_caption(self.title)

    def set_icon(self, icon):
        pygame.display.set_icon(icon.into_pygame())
        

    def fill_screen(self, color):
        self._screen.fill(color)

    def render(self, render: Render):
        render.draw_to(self._screen)

    def blit(self, blittable: Blittable, pos: Vector2):
        blittable.draw_to(self._screen, pos)

    def render_rect(self, rect, line_color, line_size):
        pygame.draw.rect(self._screen, line_color, rect, line_size)
