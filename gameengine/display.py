import math

import pygame

from ._dev_utils.classproperty import classproperty


class Display:
    surface = None
    ref_scale = pygame.math.Vector2(1, 1)

    @classmethod
    def set_scale(cls, *scale):
        cls.ref_scale = pygame.Vector2(*scale)
        try:
            window_size = pygame.display.get_surface().get_size()
            cls.surface = pygame.Surface(
                (
                    math.ceil(window_size[0] / cls.ref_scale.x),
                    math.ceil(window_size[1] / cls.ref_scale.y),
                )
            ).convert_alpha()

        except pygame.error:
            pass

    @classproperty
    def size(cls):
        return cls.surface.get_size()

    @classproperty
    def width(cls):
        return cls.surface.get_width()

    @classproperty
    def height(cls):
        return cls.surface.get_height()

    @classproperty
    def rect(cls):
        return cls.surface.get_rect()

    @classmethod
    def get_scale(cls):
        return cls.ref_scale.xy

    @classmethod
    def set_size(cls, size):
        window_size = pygame.display.get_surface().get_size()
        cls.set_scale(
            (
                window_size[0] / size[0],
                window_size[1] / size[1],
            )
        )

    @classmethod
    def get_size(cls):
        return cls.surface.get_size()

    @classmethod
    def update_display_from_window(cls):
        cls.set_scale(cls.ref_scale.xy)

    @classmethod
    def is_landscape(cls):
        return cls.width > cls.height

    @classmethod
    def is_portrait(cls):
        return not cls.is_landscape()
