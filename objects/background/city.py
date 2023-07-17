from constants import Graphics
from gamestate import GameState
from objects.background.scrolltile import ScrollTile


class City(ScrollTile):
    def __init__(self, program):
        super().__init__(
            program, GameState.Config.city_parallax_coeff, Graphics.BG_CITY
        )
