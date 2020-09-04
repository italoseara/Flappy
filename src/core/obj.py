from .data import FrameManager, Vector2D

class Renderable:
    def render(self):
        return self.frames.current_frame, self.pos.to_tuple()

class Object(Renderable):
    """The basis for most interactive elements of the game."""

    def __init__(self, pos, frames, data_space):
        """Replacement of this function is recommended, but remember to call the self._setup function at the very beginning."""
        self.setup(pos, frames, data_space)

    def setup(self, pos, frames, data_space):
        self.pos = Vector2D(*pos)
        self.frames = FrameManager.create(frames)
        self.d = data_space

    def process(self):
        """Function made in order to group code related to the object to be called once per frame."""
        pass

