from constants import CLOUDS_PARALLAX_COEFF

from .scenaryobject import ScenaryObject


class Clouds(ScenaryObject):
    def __init__(self):
        super().__init__("BG_CLOUDS", CLOUDS_PARALLAX_COEFF)
