from os.path import abspath

import pygame

from .files import get as get_file


def load_from_file(size, path):
    return pygame.font.Font(abspath(path), size)


def get_from_file_buffer(name, size):
    return pygame.Font(get_file(name), int(size))
