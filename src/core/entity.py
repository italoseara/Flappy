from .data import FrameManager, Vector2D

class Renderable:
    def render(self):
        return self.frames.current_frame, self.pos.to_tuple()

class Entity(Renderable):
    """The basis for most interactive elements of the game."""

    def __init__(self, pos, frames):
        """The replacement of this function is recommended, but remember to call the self._setup function at the very beginning."""
        self.setup(pos, frames)

    def setup(self, pos, frames):
        self.pos = Vector2D(*pos)
        self.frames = FrameManager(frames)

    def process(self):
        """A function made in order to group code related to the object to be called once per frame. Implementation is required by children of this class."""
        raise NotImplementedError

