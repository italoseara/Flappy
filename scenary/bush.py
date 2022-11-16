from constants import BUSH_PARALLAX_COEFF, SCROLL_SPEED
from .scenaryobject import ScenaryObject
from gameengine import GameEngine


class Bush(ScenaryObject):
    def __init__(self):
        super().__init__("BG_BUSH")

    def update(self):
        super().update()

        self.pos.x -= BUSH_PARALLAX_COEFF * SCROLL_SPEED * GameEngine.deltatime
        self.pos.x %= -self.origin_surface_width
        self.rect.topleft = self.pos.xy
