from os.path import abspath

import pygame

sounds = {}


def load_from_file(path):
    return pygame.mixer.Sound(abspath(path))


def add_from_file(name, path):
    sounds[name] = load_from_file(path)


def get(name):
    return sounds[name]
