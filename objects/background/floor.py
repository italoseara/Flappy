from constants import Graphics
from gamestate import GameState
from objects.background.scrolltile import ScrollTile


class Floor(ScrollTile):
    def __init__(self, program):
        super().__init__(
            program, GameState.Config.floor_parallax_coeff, Graphics.FLOOR, True
        )
