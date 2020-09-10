import pygame

from pathlib import Path

from .config import GameConfig

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

        self.blit_base_color = make_color(config.blit_base_color)
        self.score_text_font_color = make_color(config.score_text_font_color)

        self.blit_base_color = pygame.Color(*config.blit_base_color)
        self.score_text_font_color = pygame.Color(config.score_text_font_color)
        self.score_text_font = pygame.font.SysFont(
            config.score_text_font_name,
            config.score_text_font_size,
        )

    def get_resource(self, resource_name):
        return self.resources[resource_name]

def make_color(arg):
    if isinstance(arg, tuple):
        return pygame.Color(*arg)
    return pygame.Color(arg)
