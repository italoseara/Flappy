from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True)
class GameConfig:
    """Contains the game configuration."""

    resources_dir: str
    resources_to_load: List[Tuple[str, str]]

    title: str
    debug_mode: bool
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
