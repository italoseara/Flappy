import pygame

from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from core.data import Blittable

class GameMode(Enum):
    START = 0
    PLAYING = 1
    DEAD = 2

class GameCache:
    """Contains game cache, helping with speed."""
    def __init__(self, config):
        assert isinstance(config, GameConfig)

        # Carregar arquivos de imagem
        self.resources = {}
        rdir = Path(config.resources_dir)
        for pre_resource in config.resources_to_load:
            name, filename = pre_resource
            fpath = rdir / filename
            with open(fpath, "r") as f:
                self.resources[str(name)] = config.resources_wrapper(pygame.image.load(f))

        self.blit_base_color = _make_color(config.blit_base_color)
        self.score_text_font_color = _make_color(config.score_text_font_color)
        self.score_text_font = pygame.font.SysFont(
            config.score_text_font_name,
            config.score_text_font_size,
        )

    def get_resource(self, resource_name):
        return self.resources[resource_name]

def _make_color(arg):
    if isinstance(arg, tuple):
        return pygame.Color(*arg)
    return pygame.Color(arg)


@dataclass(frozen=True)
class GameConfig:
    """Contains the game configuration."""

    resources_dir: str
    resources_wrapper: Blittable
    resources_to_load: List[Tuple[str, str]]

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
