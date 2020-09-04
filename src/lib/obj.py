from .data import FrameManager, Vector2D

class Object:
    """É a base para grande parte dos elementos interativos no jogo."""

    def __init__(self, pos, frames, data_space):
        """Inicia o objeto quando ele é criado.
        
        A substituição desta função é recomendada, mas lembre-se de chamar a função self._setup logo no início dela.
        """
        self.setup(pos, frames, data_space)

    def setup(self, pos, frames, data_space):
        self.pos = Vector2D(*pos)
        self.frames = FrameManager.create(frames)
        self.d = data_space

    def process(self):
        """Função feita com o intuito de agrupar código relacionado ao objeto para ser chamado uma vez por frame."""
        pass

    def render(self) -> tuple:
        """Compila e retorna uma tupla: (frame a ser renderizado, posição)"""
        return self.frames.current_frame, self.pos.to_tuple()
