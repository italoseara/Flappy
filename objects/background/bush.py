from constants import Graphics
from gamestate import GameState
from objects.background.scrolltile import ScrollTile


class Bush(ScrollTile):
    def __init__(self, program):
        super().__init__(
            program, GameState.Config.bush_parallax_coeff, Graphics.BG_BUSH
        )
