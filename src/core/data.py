import pygame

class FrameManager:
    """Uma lista de imagens com variáveis relacionadas à renderização."""

    def __init__(self, frames, current_index=0):
        self.frame_list = list(frames)
        self.current_index = current_index

    @property
    def current_frame(self):
        return self.frame_list[self.current_index]

class Vector2D:
    """Um vetor de duas dimensões."""
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    @property
    def x(self):
        return self._raw_x

    @x.setter
    def x(self, value):
        self._raw_x = float(value)

    @property
    def y(self):
        return self._raw_y

    @y.setter
    def y(self, value):
        self._raw_y = float(value)

    def to_tuple(self) -> tuple:
        return (self.x, self.y)

def resource_dict(resource_list):
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
