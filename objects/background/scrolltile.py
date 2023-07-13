from math import ceil

from constants import GameMode
from gameengine.basechild import BaseChild
from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.resources import Resources
from gamestate import GameState


class ScrollTile(BaseChild):
    def __init__(self, coeff, tile, floor=False):
        surf = Resources.Surface.get(tile)
        self.surf_w = surf.get_width()
        surf_h = surf.get_height()

        super().__init__(Resources.Surface.new((Display.width + self.surf_w, surf_h)))

        ground_y = GameState.Config.ground_line
        if floor:
            self.rect.y = ground_y
        else:
            self.rect.bottom = ground_y

        self.speed_x = -GameState.Config.scroll_speed * coeff

        for i in range(ceil(Display.width / self.surf_w) + 1):
            self.image.blit(surf, (i * self.surf_w, 0))

    def update(self):
        if GameState.game_mode != GameMode.DEAD:
            super().update()

            self.rect.x += self.speed_x * Engine.deltatime
            self.rect.x %= -self.surf_w
