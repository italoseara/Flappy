from math import ceil

from gameengine.basechild import BaseChild
from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.resources import Resources
from gamestate import GameState


class ScrollTile(BaseChild):
    def __init__(self, coeff, tile):
        surf = Resources.Surface.get(tile)
        self.surf_w = surf.get_width()
        surf_h = surf.get_height()

        super().__init__(Resources.Surface.new((Display.width + self.surf_w, surf_h)))

        self.rect.bottom = GameState.Config.ground_line

        self.speed_x = -GameState.Config.scroll_speed * coeff

        for i in range(ceil(Display.width / self.surf_w) + 1):
            self.image.blit(surf, (i * self.surf_w, 0))

    def update(self):
        super().update()

        self.rect.x += self.speed_x * Engine.deltatime
        self.rect.x %= -self.surf_w
