import state
from constants import Graphics
from objects.background.scrolltile import ScrollTile


class City(ScrollTile):
    def __init__(self):
        super().__init__(state.config.city_parallax_coeff, Graphics.BG_CITY)
