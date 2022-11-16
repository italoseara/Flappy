from pprint import pp

import pygame
import pygame._sdl2


class Window:
    _sdl2_window = None
    window_surface = None

    @classmethod
    def get_size(cls):
        return cls._sdl2_window.size

    @classmethod
    def set_size(cls, size, *flags):
        flag = 0
        for f in flags:
            flag |= f
        cls.window_surface = pygame.display.set_mode(size, flag)
        Window._sdl2_window = pygame._sdl2.Window.from_display_module()

    @classmethod
    def set_title(cls, title):
        pygame.display.set_caption(title)

    @classmethod
    def get_title(cls):
        return cls._sdl2_window.title

    @classmethod
    def get_window_sdl2(cls):
        return cls._sdl2_window
