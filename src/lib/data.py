"""Classes para armazenamento de dados (data structures)."""

import pygame

class FrameManager:
    """Uma lista de imagens com variáveis relacionadas à renderização."""

    def __init__(self, frames: list = [], current_index: int = 0):
        self.frame_list = frames
        self.current_index = current_index

    @property
    def current_frame(self):
        return self.frame_list[self.current_index]

    @staticmethod
    def create(arg):
        assert type(arg) in {tuple, list, pygame.Surface}
        if type(arg) in {tuple, list}:
            return FrameManager(list(arg))
        elif type(arg) == pygame.Surface:
            return FrameManager([arg])

class Vector2D:
    """Um vetor de duas dimensões."""
    def __init__(self, x=0.0, y=0.0) -> None:
        self.x = float(x)
        self.y = float(y)

    @property
    def x(self):
        return self._raw_x

    @x.setter
    def x(self, value):
        assert type(value) in {int, float}, "o tipo do valor dado a x deve ser int ou float"
        self._raw_x = value

    @property
    def y(self):
        return self._raw_y

    @y.setter
    def y(self, value):
        assert type(value) in {int, float}, "o tipo do valor dado a y deve ser int ou float"
        self._raw_y = value

    @staticmethod
    def create(tup: tuple):
        """Retorna um Vector2D baseado em uma tupla de dois números (float ou int)."""
        assert len(tup) == 2, "a tupla deve ter somente dois elementos"
        assert (type(tup[0]) == type(tup[1]) == float) or (type(tup[0]) == type(tup[1]) == int), "o tipo de ambos os elementos na tupla devem ser `float` ou `int`"
        return Vector2D(*tup)

    def to_tuple(self) -> tuple:
        return (self.x, self.y)

class ResourceList:
    """Uma lista de recursos (atualmente só imagens) para jogos. Classe sem instâncias."""

    @staticmethod
    def create(resource_list: tuple):
        """Carrega as imagens providenciadas na lista de tuplas `resource_list`.

        resource_list = [(nome, caminho_da_imagem), (nome, caminho_da_imagem), ...]
        """
        value_to_return = {}
        for resource in resource_list:
            assert len(resource) == 2, "a tupla só pode ter dois elementos"

            name = resource[0]
            resource_path = resource[1]
            assert type(name) == type(resource_path) == str, "o tipo dos elementos da tupla deve ser str"
            
            value_to_return[name] = pygame.image.load(resource_path)
        return value_to_return
