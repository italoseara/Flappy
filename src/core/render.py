from .maths import Vector2
from .data import PygameSurface, Blittable

import abc
from pygame import Surface
from typing import List, Tuple

class Render:
    @abc.abstractmethod
    def draw_to(self, surface: Surface) -> None: ...

class SingularRender(Render):
    @abc.abstractmethod
    def get_render(self) -> Tuple[PygameSurface, Vector2]: ...

    def draw_to(self, surface: Surface) -> None:
        render, position = self.get_render()
        render.draw_to(surface, position)

class BatchRender(Render):
    @abc.abstractmethod
    def get_render(self) -> List[Tuple[Blittable, Vector2]]: ...

    def draw_to(self, surface: Surface) -> None:
        for (render, position) in self.get_render():
            render.draw_to(surface, position)
