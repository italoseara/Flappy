import pygame


class GameResources:
    scenes = {}
    animations = {}
    surfaces = {}

    @classmethod
    def add_scene(cls, name, pygame_group, *args, **kwargs):
        def call_scene():
            return pygame_group(*args, **kwargs)

        cls.scenes[name] = call_scene

    @classmethod
    def get_scene(cls, name):
        return cls.scenes[name]()

    @classmethod
    def add_animation_data(cls, name, animation):
        cls.animations[name] = animation

    @classmethod
    def get_animation_data(cls, name):
        return cls.animations[name]

    @classmethod
    def add_surface_from_file(cls, name, path, alpha=True):
        surface = pygame.image.load(path)
        if alpha:
            surface = surface.convert_alpha()
        else:
            surface = surface.convert()
        cls.add_surface(name, surface, copy=False)

    @classmethod
    def add_surface(cls, name, surface, copy=True):
        if copy:
            surface = surface.copy()
        cls.surfaces[name] = surface

    @classmethod
    def get_surface(cls, name, copy=True):
        surface = cls.surfaces[name]
        if copy:
            return surface.copy()
        else:
            return surface

    @staticmethod
    def get_new_surface(size, *flags, alpha=True):
        flag = 0
        for f in flags:
            if f != pygame.SRCALPHA:
                flag |= f
        if alpha:
            flag |= pygame.SRCALPHA
        return pygame.Surface(size, flag)
