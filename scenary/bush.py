from constants import BUSH_PARALLAX_COEFF

from .scenaryobject import ScenaryObject


class Bush(ScenaryObject):
    def __init__(self):
        super().__init__("BG_BUSH", BUSH_PARALLAX_COEFF)
