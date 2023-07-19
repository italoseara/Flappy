import state
from constants import Graphics
from objects.background.scrolltile import ScrollTile


class Floor(ScrollTile):
    def __init__(self):
        super().__init__(state.config.floor_parallax_coeff, Graphics.FLOOR, True)
