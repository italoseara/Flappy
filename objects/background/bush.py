from constants import Graphics
from gamestate import GameState
from objects.background.scrolltile import ScrollTile


class Bush(ScrollTile):
    def __init__(self):
        super().__init__(GameState.Config.bush_parallax_coeff, Graphics.BG_BUSH)
