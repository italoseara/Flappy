from .maths import Vector2
from pygame import Surface

from typing import List

class Blittable:
    @property
    def size(self) -> Vector2:
        raise NotImplementedError

    def draw_to(self, other_surface: Surface, pos: tuple):
        raise NotImplementedError

class PygameSurface(Blittable):
    def __init__(self, surface: Surface):
        self.inner = surface

    @property
    def size(self) -> Vector2:
        return Vector2(self.inner.get_rect().size)

    def draw_to(self, other_surface: Surface, pos: tuple):
        other_surface.blit(self.inner, tuple(pos))

    def into_pygame(self):
        return self.inner

class FrameManager:
    """Manages a list of frames."""
    def __init__(self, frames, current_index=0):
        self.frame_list: List[Blittable] = list(frames)
        self.current_index = current_index

    @property
    def current_frame(self):
        return self.frame_list[self.current_index]
