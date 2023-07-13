from constants import Graphics
from gamestate import GameState
from objects.scrolltile import ScrollTile


class City(ScrollTile):
    def __init__(self):
        super().__init__(GameState.Config.city_parallax_coeff, Graphics.BG_CITY)
