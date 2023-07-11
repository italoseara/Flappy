import pygame

from ._dev_utils import classproperty


class Window:
    surface = None
    size = (1, 1)

    @classmethod
    def get_size(cls):
        return cls.surface.get_size()

    @classmethod
    def set_size(cls, size, *flags):
        flag = pygame.SRCALPHA
        for f in flags:
            flag |= f
        cls.surface = pygame.display.set_mode(size, flag)

    @classmethod
    def set_title(cls, title):
        pygame.display.set_caption(title)

    @classmethod
    def set_icon(cls, icon):
        pygame.display.set_icon(icon)

    @classmethod
    def get_title(cls):
        return pygame.display.get_caption()

    @classproperty
    def size(self):
        return self.surface.get_size()

    @classproperty
    def width(self):
        return self.surface.get_width()

    @classproperty
    def height(self):
        return self.surface.get_height()

    @classproperty
    def rect(self):
        return self.surface.get_rect()

    @classmethod
    def is_landscape(cls):
        return cls.width > cls.height

    @classmethod
    def is_portrait(cls):
        return not cls.is_landscape()
