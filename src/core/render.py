from .maths import Vector2

from typing import List, Tuple
from pygame import Surface

class Render:
    def draw_to(self, surface: Surface):
        raise NotImplementedError

class SingularRender(Render):
    def get_render(self) -> Tuple[Surface, Vector2]:
        raise NotImplementedError

    def draw_to(self, surface: Surface):
        render, position = self.get_render()
        render.draw_to(
            surface,
            (int(position[0]), int(position[1])),
        )

class BatchRender(Render):
    def get_render(self) -> Tuple[List[Surface], Vector2]:
        raise NotImplementedError

    def draw_to(self, surface: Surface):
        for (render, position) in self.get_render():
            render.draw_to(
                surface,
                (int(position[0]), int(position[1])),
            )
