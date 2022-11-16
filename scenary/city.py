from constants import CITY_PARALLAX_COEFF, SCROLL_SPEED
from .scenaryobject import ScenaryObject
from gameengine import GameEngine


class City(ScenaryObject):
    def __init__(self):
        super().__init__("BG_CITY")

    def update(self):
        super().update()

        self.pos.x -= CITY_PARALLAX_COEFF * SCROLL_SPEED * GameEngine.deltatime
        self.pos.x %= -self.origin_surface_width
        self.rect.topleft = self.pos.xy
