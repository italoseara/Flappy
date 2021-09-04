from .data import FrameManager, PygameSurface, Blittable
from .maths import Vector2
from .render import SingularRender

from typing import Tuple, List
from pygame import Rect, Surface

class SimpleEntity(SingularRender):
    """The basis for most interactive elements of the game."""

    def __init__(self, pos: Vector2, frames: List[Blittable]):
        self.pos = pos
        self.frames = FrameManager(frames)

    def process(self, state):
        """Made in order to group code related to the object to be called once per frame.
        Implementation is required by children of this class.
        """
        raise NotImplementedError

    @property
    def hitbox(self) -> Rect:
        return Rect(
            self.pos.to_tuple(),
            self.frames.current_frame.size.to_tuple(),
        )

    def get_render(self) -> Tuple[PygameSurface, Vector2]:
        return (self.frames.current_frame, self.pos)
