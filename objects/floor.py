from constants import Graphics
from gamestate import GameState
from objects.scrolltile import ScrollTile


class Floor(ScrollTile):
    def __init__(self):
        super().__init__(GameState.Config.floor_parallax_coeff, Graphics.FLOOR, True)
