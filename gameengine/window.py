import math

import pygame


class Metrics:
    @property
    def size(self):
        return self.surface.get_size()

    @property
    def width(self):
        return self.surface.get_width()

    @property
    def height(self):
        return self.surface.get_height()

    @property
    def rect(self):
        return self.surface.get_rect()

    @property
    def is_landscape(self):
        return self.width > self.height

    @property
    def is_portrait(self):
        return self.height > self.width


class Display(Metrics):
    window = None
    surface = None
    __scale = None

    def __init__(self, size, window):
        self.window = window
        self.set_size(size)

    def set_size(self, size):
        self.set_scale((self.window.size[0] / size[0], self.window.size[1] / size[1]))

    def set_scale(self, *scale):
        self.__scale = pygame.Vector2(*scale).xy
        try:
            self.surface = pygame.Surface(
                (
                    math.ceil(self.window.size[0] / self.__scale.x),
                    math.ceil(self.window.size[1] / self.__scale.y),
                )
            ).convert_alpha()
        except pygame.error as err:
            print(err)

    @property
    def scale(self):
        return self.__scale


class Window(Metrics):
    surface = None
    display = None

    def __init__(self, size=(1, 1), *flags):
        self.set_size(size, *flags)
        self.display = Display(size, self)

    def update(self):
        if self.display.size != self.size:
            pygame.transform.scale(
                self.display.surface,
                self.size,
                self.surface,
            )
        else:
            self.surface.blit(self.display.surface, (0, 0))
        pygame.display.update()

    def set_size(self, size, *flags):
        flag = pygame.SRCALPHA
        for f in flags:
            flag |= f
        self.surface = pygame.display.set_mode(size, flag)

    def set_title(self, title):
        pygame.display.set_caption(title)

    def get_title(self):
        return pygame.display.get_caption()

    def set_icon(self, icon):
        pygame.display.set_icon(icon)
