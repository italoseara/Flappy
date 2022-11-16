import math

import pygame

from gameengine import Display, GameResources

from constants import GROUND_LINE


class ScenaryObject(pygame.sprite.DirtySprite):
    def __init__(self, surface_name, ignore_cloud_line=False):
        super().__init__()
        surface = GameResources.Surface.get_surface(surface_name)
        s_size = surface.get_size()

        cloud_rect = GameResources.Surface.get_surface("BG_CLOUDS").get_rect()
        w = math.ceil(Display.get_size()[0] / s_size[0]) + 1
        self.image = GameResources.Surface.get_new_surface((w * s_size[0], s_size[1]))

        for i in range(w):
            self.image.blit(surface, (i * s_size[0], 0))

        self.origin_surface_width = s_size[0]
        self.pos = pygame.Vector2(0, 0)
        self.dirty = 2

        self.rect = self.image.get_rect()
        cloud_h = cloud_rect.h

        if ignore_cloud_line:
            cloud_h = 0
        self.pos.y = GROUND_LINE - cloud_h
