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
                self.resources[str(name)] = pygame.image.load(f)

        self.background_color = make_color(config.background_color)
        self.score_font_color = make_color(config.score_font_color)


        self.background_color = pygame.Color(*config.background_color)
        self.score_font_color = pygame.Color(config.score_font_color)
        self.score_font = pygame.font.SysFont(config.score_font_name, config.score_font_size)

    def get_resource(self, resource_name):
        return self.resources[resource_name]

def make_color(arg):
    if type(arg) == tuple:
        return pygame.Color(*arg)
    else:
        return pygame.Color(arg)
