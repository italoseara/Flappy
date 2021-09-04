from __future__ import annotations

from .maths import Vector2

import pygame
from pygame import Surface

import abc
from typing import List, cast, Union

class Blittable:
    @property
    @abc.abstractmethod
    def size(self) -> Vector2: ...

    @abc.abstractmethod
    def draw_to(self, surface: Surface, pos: Vector2) -> None: ...

class PygameSurface(Blittable):
    def __init__(self, surface: Union[pygame.Surface, pygame.surface.Surface]):
        self.inner = surface

    @property
    def size(self) -> Vector2:
        return Vector2.from_tuple(self.inner.get_rect().size)

    def draw_to(self, canvas: Surface, pos: Vector2) -> None:
        canvas.blit(self.inner, pos.to_tuple())

    def scaled(self, scale: Vector2) -> PygameSurface:
        return PygameSurface(pygame.transform.scale(
            self.inner,
            (int(scale.x * self.size.x), int(scale.y * self.size.y)),
        ))

    def into_pygame(self) -> Surface:
        return cast(Surface, self.inner)

class FrameManager:
    """Manages a list of frames."""
    def __init__(self, frames: List[Blittable], current_index: int = 0):
        self.frame_list = frames
        self.current_index = current_index

    @property
    def current_frame(self):
        return self.frame_list[self.current_index]
