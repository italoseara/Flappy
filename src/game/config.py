from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True)
class GameConfig:
    """Armazena as configurações do jogo."""

    # Configurações sem padrões (valores precisam ser especificados)
    resources_to_load: List[Tuple[str, str]]
    speed: int
    font_string: str
    debug_mode: bool
    title: str
    resources_dir: str

    # Configurações com padrões
    # TODO: mover a maioria dos padrões
    win_size: Tuple[int, int] = (960, 540)
    background_color: Tuple[int, int, int] = (115, 200, 215)
    framerate: int = 60
    gravity: float = 0.5
    bg_parallax: float = 0.5
    floor_parallax: float = 1.0
    hitbox_width: int = 2
    pipe_height_interval: Tuple[int, int] = (-210, -40)
    pipe_y_spacing: int = 130
    jump_speed: float = -8.0
    hitbox_color: Tuple[int, int, int] = (255, 0, 0)
    player_hitbox_color: Tuple[int, int, int] = (0, 255, 0)
    score_font_name: str = "Cascadia Code, Consolas, Tahoma"
    score_font_size: int = 20
    score_font_color: str = "white"
    score_text_enabled: bool = True
    score_text_pos: Tuple[int, int] = (15, 10)
    ground_pos: int = 476
