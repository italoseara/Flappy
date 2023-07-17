from constants import Graphics
from gamestate import GameState
from objects.background.scrolltile import ScrollTile


class Clouds(ScrollTile):
    def __init__(self):
        super().__init__(GameState.Config.clouds_parallax_coeff, Graphics.BG_CLOUDS)
