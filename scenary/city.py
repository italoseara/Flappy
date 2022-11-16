from constants import CITY_PARALLAX_COEFF

from .scenaryobject import ScenaryObject


class City(ScenaryObject):
    def __init__(self):
        super().__init__("BG_CITY", CITY_PARALLAX_COEFF)
