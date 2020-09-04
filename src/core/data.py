import pygame

class FrameManager:
    """Manages a list of frames."""

    def __init__(self, frames, current_index=0):
        self.frame_list = list(frames)
        self.current_index = current_index

    @property
    def current_frame(self):
        return self.frame_list[self.current_index]

class Vector2D:
    """A two-dimensional vector"""
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
    """Loads the images provided by `resource_list`.

    resource_list: List[Tuple[str, str]]
    The first element of each tuple is the resource name to be stored, and the second element is the image path.
    """
    value_to_return = {}
    for resource in resource_list:
        assert len(resource) == 2, "a tupla só pode ter dois elementos"

        name = resource[0]
        resource_path = resource[1]
        assert type(name) == type(resource_path) == str, "o tipo dos elementos da tupla deve ser str"
        
        value_to_return[name] = pygame.image.load(resource_path)
    return value_to_return
