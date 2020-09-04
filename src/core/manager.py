import pygame

from .maths import gameobject_render

class GameManager:
    def __init__(self, title, win_size, icon):
        self.title = title
        self.win_size = win_size

        self._screen = pygame.display.set_mode(self.win_size)
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(icon)

    def fill_screen(self, color):
        self._screen.fill(color)

    def blit(self, thing, pos):
        self._screen.blit(thing, pos)

    def render(self, obj):
        gameobject_render(obj, self._screen)
