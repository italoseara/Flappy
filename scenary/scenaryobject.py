import math

import pygame

from constants import GROUND_LINE, SCROLL_SPEED
from gameengine import Display, GameEngine, GameResources


class ScenaryObject(pygame.sprite.DirtySprite):
    def __init__(self, surface_name, coeff, ignore_cloud_line=False):
        super().__init__()
        self.coeff = coeff
        surface = GameResources.Surface.get_surface(surface_name)
        s_size = surface.get_size()
        cloud_rect = GameResources.Surface.get_surface("BG_CLOUDS").get_rect()
        cloud_h = cloud_rect.h
        if ignore_cloud_line:
            cloud_h = 0
        self.pos = pygame.Vector2(0, 0)
        self.pos.y = GROUND_LINE - cloud_h

        # makes the surface continuous
        w = math.ceil(Display.get_size()[0] / s_size[0]) + 1
        self.image = GameResources.Surface.get_new_surface((w * s_size[0], s_size[1]))

        for i in range(w):
            self.image.blit(surface, (i * s_size[0], 0))

        self.origin_surface_width = s_size[0]
        self.rect = self.image.get_rect()


        self.dirty = 2

    def update(self):
        super().update()

        self.pos.x -= self.coeff * SCROLL_SPEED * GameEngine.deltatime
        self.pos.x %= -self.origin_surface_width
        self.rect.topleft = self.pos.xy
