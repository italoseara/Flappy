from os.path import abspath

import pygame

surfaces = {}


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


def add_from_file(name, path, alpha=True):
    set(name, load_from_file(path, alpha))


def set(name, surface, copy=False):
    if copy:
        surface = surface.copy()
    surfaces[name] = surface


def slice(name, *rects):
    surface = get(name)
    return [surface.subsurface(rect).copy() for rect in rects]


def get(name, copy=True):
    surface = surfaces[name]
    if copy:
        return surface.copy()
    else:
        return surface


def new(size, *flags, alpha=True):
    flag = 0
    for f in flags:
        if f != pygame.SRCALPHA:
            flag |= f
    if alpha:
        flag |= pygame.SRCALPHA
    return pygame.Surface(size, flag)
