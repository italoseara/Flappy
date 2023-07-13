from constants import DEFAULT_WIN_SIZE, GameMode


class GameState:
    is_paused = False
    game_mode = GameMode.START

    class Config:
        gravity = 1410
        ground_line = DEFAULT_WIN_SIZE.y - 64
        jump_speed = -400
        scroll_speed = 200
        clouds_parallax_coeff = 0.1
        city_parallax_coeff = 0.3
        bush_parallax_coeff = 0.4
