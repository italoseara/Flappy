from constants import FLOOR_PARALLAX_COEFF, SCROLL_SPEED

from .scenaryobject import ScenaryObject
from gameengine import GameEngine


class Floor(ScenaryObject):
    def __init__(self):
        super().__init__("FLOOR", True)

    def update(self):
        super().update()

        self.pos.x -= FLOOR_PARALLAX_COEFF * SCROLL_SPEED * GameEngine.deltatime
        self.pos.x %= -self.origin_surface_width
        # self.pos.x -= self.origin_surface_width
        self.rect.topleft = self.pos.xy
