from constants import GameMode


class GameState:
    is_paused = False
    game_mode = GameMode.START

    class Config:
        gravity = 1410
