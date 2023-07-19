from math import ceil

import state
from constants import GameMode
from gameengine import resources
from gameengine.basechild import BaseChild


class ScrollTile(BaseChild):
    def __init__(self, coeff, tile, floor=False):
        surf = resources.surface.get(tile)
        self.surf_w = surf.get_width()
        surf_h = surf.get_height()

        display = self.program.window.display

        super().__init__(resources.surface.new((display.width + self.surf_w, surf_h)))

        ground_y = state.config.ground_line
        if floor:
            self.rect.y = ground_y
        else:
            self.rect.bottom = ground_y

        self.speed_x = -state.config.scroll_speed * coeff

        for i in range(ceil(display.width / self.surf_w) + 1):
            self.surface.blit(surf, (i * self.surf_w, 0))

    def update(self):
        if state.game_mode != GameMode.DEAD and not state.is_paused:
            super().update()

            self.rect.x += self.speed_x * self.program.time.delta
            self.rect.x %= -self.surf_w
