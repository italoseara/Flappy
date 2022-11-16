import math

import pygame


class Display:
    display_surface = None
    background = None
    ref_scale = pygame.math.Vector2(1, 1)

    @classmethod
    def set_scale(cls, *scale):
        cls.ref_scale = pygame.Vector2(*scale)
        try:
            window_size = pygame.display.get_window_size()
            cls.display_surface = pygame.Surface(
                (
                    math.ceil(window_size[0] / cls.ref_scale.x),
                    math.ceil(window_size[1] / cls.ref_scale.y),
                )
            ).convert_alpha()

        except pygame.error:
            ...

    @classmethod
    def get_scale(self):
        return self.ref_scale.xy

    @classmethod
    def set_size(cls, size):
        window_size = pygame.display.get_window_size()
        cls.set_scale(
            (
                window_size[0] / size[0],
                window_size[1] / size[1],
            )
        )

    @classmethod
    def get_size(cls):
        return cls.display_surface.get_size()

    @classmethod
    def set_display_from_window(cls):
        cls.set_scale(cls.ref_scale.xy)
