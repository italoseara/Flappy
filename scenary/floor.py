from constants import FLOOR_PARALLAX_COEFF

from .scenaryobject import ScenaryObject


class Floor(ScenaryObject):
    def __init__(self):
        super().__init__("FLOOR", FLOOR_PARALLAX_COEFF, ignore_cloud_line=True)
