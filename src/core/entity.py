from .data import FrameManager
from .maths import Vector2
from .render import SingularRender

from pygame import Rect

class SimpleEntity(SingularRender):
    """The basis for most interactive elements of the game."""

    def __init__(self, pos, frames):
        self.pos = Vector2(pos)
        self.frames = FrameManager(frames)

    def process(self):
        """Made in order to group code related to the object to be called once per frame.
        Implementation is required by children of this class.
        """
        raise NotImplementedError

    @property
    def hitbox(self):
        return Rect(
            tuple(self.pos),
            tuple(self.frames.current_frame.size),
        )

    def get_render(self):
        return (
            self.frames.current_frame,
            (int(self.pos.x), int(self.pos.y))
        )
