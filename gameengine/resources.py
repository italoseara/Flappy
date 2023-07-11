from os.path import abspath

import pygame
from io import BytesIO


class Resources:
    class Scenes:
        scenes = {}

        @classmethod
        def add(cls, name, pygame_group, *args, **kwargs):
            def call():
                return pygame_group(*args, **kwargs)

            cls.scenes[name] = call

        @classmethod
        def get(cls, name):
            return cls.scenes[name]()

    class Surface:
        surfaces = {}

        @staticmethod
        def load_from_file(path, alpha=True):
            surface = pygame.image.load(abspath(path))
            try:
                if alpha:
                    surface = surface.convert_alpha()
                else:
                    surface = surface.convert()
                return surface
            except pygame.error:
                return surface

        @classmethod
        def add_from_file(cls, name, path, alpha=True):
            cls.set(name, cls.load_from_file(path, alpha))

        @classmethod
        def set(cls, name, surface, copy=False):
            if copy:
                surface = surface.copy()
            cls.surfaces[name] = surface

        @classmethod
        def slice(cls, name, *rects):
            surface = cls.get(name)
            return [surface.subsurface(rect).copy() for rect in rects]

        @classmethod
        def contains(cls, key):
            return key in cls.surfaces.keys()

        @classmethod
        def get(cls, name, copy=True) -> pygame.Surface:
            surface = cls.surfaces[name]
            if copy:
                return surface.copy()
            else:
                return surface

        @classmethod
        def new(cls, size, *flags, alpha=True):
            flag = 0
            for f in flags:
                if f != pygame.SRCALPHA:
                    flag |= f
            if alpha:
                flag |= pygame.SRCALPHA
            return pygame.Surface(size, flag)

    class Files:
        files = {}

        @classmethod
        def add_from_path(cls, name, path):
            with open(abspath(path), "rb") as font_file:
                cls.files[name] = font_file.read()

        @classmethod
        def get(cls, name):
            return BytesIO(cls.files[name])

    class Fonts:
        @classmethod
        def load_from_file(cls, size, path):
            return pygame.font.Font(abspath(path), size)

        @classmethod
        def get_from_file_buffer(cls, name, size):
            return pygame.Font(Resources.Files.get(name), int(size))
