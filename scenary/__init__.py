import pygame

from .bush import Bush
from .city import City
from .clouds import Clouds
from .floor import Floor


class ScenaryGroup(pygame.sprite.LayeredDirty):
    def __init__(self):
        super().__init__(
            Floor(),
            Clouds(),
            City(),
            Bush(),
        )
