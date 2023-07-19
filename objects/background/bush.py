import state
from constants import Graphics
from objects.background.scrolltile import ScrollTile


class Bush(ScrollTile):
    def __init__(self):
        super().__init__(state.config.bush_parallax_coeff, Graphics.BG_BUSH)
