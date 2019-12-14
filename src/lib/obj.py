"""Arquivo contendo duas classes: Object e Game."""

# import pygame
from lib.data import FrameManager, Vector2D, ResourceList

class Object:
    """É a base para grande parte dos elementos interativos no jogo."""

    def __init__(self, pos=(0,0), frames=[], linked_game=None):
        """Inicia o objeto quando ele é criado.
        
        A substituição desta função é recomendada, mas lembre-se de chamar a função self._setup logo no início dela.
        """
        self.setup(pos, frames, linked_game)

    def setup(self, pos, frames, linked_game):
        self.pos = Vector2D.create(pos)
        self.frames = FrameManager.create(frames)
        self.linked_game = linked_game

    def process(self):
        """Função feita com o intuito de agrupar código relacionado ao objeto para ser chamado uma vez por frame."""
        pass

    def render(self) -> tuple:
        """Compila e retorna uma tupla: (frame a ser renderizado, posição)"""
        return self.frames.current_frame, self.pos.to_tuple()

class Game:
    """O objeto-base do jogo."""

    def __init__(self, resource_data: list):
        """Prepara e inicia o jogo.

        A substituição desta função é recomendada, mas lembre-se de chamar a função self.setup logo no início dela.
        """
        self.setup(resource_data)

    def setup(self, resource_data: list):
        self.res = ResourceList.create(resource_data)
