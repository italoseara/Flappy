from .data import FrameManager
from .maths import Vector2

class Renderable:
    def render(self):
        raise NotImplementedError

class Entity(Renderable):
    """The basis for most interactive elements of the game."""

    def __init__(self, pos, frames):
        self.pos = Vector2.from_tuple(pos)
        self.frames = FrameManager(frames)

    def process(self):
        """Made in order to group code related to the object to be called once per frame.
        Implementation is required by children of this class.
        """
        raise NotImplementedError

    def render(self):
        x, y = self.pos.into_tuple()
        return (self.frames.current_frame, (int(x), int(y)))

