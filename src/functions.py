#!/usr/bin/env python3

"""Algumas ferramentas úteis para o jogo."""

from pygame import Rect


def image_size(image):
    """Obtém o tamanho de uma imagem."""
    return image.get_rect().size


def image_rectangle(image):
    """Obtém o retângulo de uma imagem."""
    return Rect((0, 0) + image_size(image))


def gameobject_size(gameobject):
    """Obtém o tamanho de um GameObject."""
    return image_size(gameobject.frame_list[0])


def gameobject_hitbox(gameobject):
    """Obtém um retângulo de um GameObject com tamanho da sua imagem e sua posição."""
    return Rect(tuple(gameobject.pos) + image_size(gameobject.frame_list[0]))


def gameobject_render(gameobject, screen):
    """Renderiza um GameObject."""
    screen.blit(*gameobject.compile_render())
