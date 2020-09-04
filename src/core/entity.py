from .data import FrameManager, Vector2D

class Renderable:
    def render(self):
        return self.frames.current_frame, self.pos.to_tuple()

class Entity(Renderable):
    """A base para a maioria dos elementos interativos no jogo."""

    def __init__(self, pos, frames):
        """A substituição desta função é recomendada, mas lembre-se de chamar a função self._setup logo no início dela."""
        self.setup(pos, frames)

    def setup(self, pos, frames):
        self.pos = Vector2D(*pos)
        self.frames = FrameManager(frames)

    def process(self):
        """Função feita com o intuito de agrupar código relacionado ao objeto para ser chamado uma vez por frame."""
        raise NotImplementedError

