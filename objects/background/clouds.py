import state
from constants import Graphics
from objects.background.scrolltile import ScrollTile


class Clouds(ScrollTile):
    def __init__(self):
        super().__init__(state.config.clouds_parallax_coeff, Graphics.BG_CLOUDS)
