from enum import Enum, IntEnum, unique, auto
from dataclasses import dataclass
from typing import Tuple

class GameMode(Enum):
    START = 0
    PLAYING = 1
    DEAD = 2

@dataclass(frozen=True)
class GameConfig:
    """Contains the game configuration."""
    title: str
    debug_mode_default: bool
    framerate: int
    gravity: float

    scroll_speed: int
    jump_speed: float
    win_size: Tuple[int, int]
    blit_base_color: Tuple[int, int, int]

    score_text_font_name: str
    score_text_font_size: int
    score_text_font_color: str
    score_text_enabled: bool
    score_text_pos: Tuple[int, int]

    hitbox_line_size: int
    hitbox_line_color: Tuple[int, int, int]

    clouds_parallax_coeff: float
    bush_parallax_coeff: float
    city_parallax_coeff: float
    floor_parallax_coeff: float

    pipe_y_offset_range: Tuple[int, int]
    pipe_y_spacing: int
    pipe_x_spacing: int

    ground_line: int

@unique
class Gfx(IntEnum):
    ICON = auto()

    CHAR_0 = auto()
    CHAR_1 = auto()
    CHAR_2 = auto()
    CHAR_3 = auto()
    CHAR_4 = auto()
    CHAR_5 = auto()
    CHAR_6 = auto()
    CHAR_7 = auto()
    CHAR_8 = auto()
    CHAR_9 = auto()

    FLOOR = auto()
    BG_BUSH = auto()
    BG_CITY = auto()
    BG_CLOUDS = auto()
    PIPE_TOP = auto()
    PIPE_BOT = auto()

    BIRD_F0 = auto()
    BIRD_F1 = auto()
    BIRD_F2 = auto()

    MSG_GAME_OVER = auto()
    MSG_FLAPPY = auto()
    MSG_READY = auto()

    BTN_PAUSE_NORMAL = auto()
    BTN_PAUSE_PAUSED = auto()
    BTN_PLAY = auto()
    BTN_SCOREBOARD = auto()

    BOX_MENU = auto()
    BOX_END = auto()

    STARTER_TIP = auto()

@unique
class Aud(IntEnum):
    WING = auto()
    HIT = auto()
    POINT = auto()
    DIE = auto()
