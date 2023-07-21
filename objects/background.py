from math import ceil

import state
from constants import GameMode, Graphics
from gameengine import resources
from gameengine.graphicnode import GraphicNode


class BatchTile(GraphicNode):
    def __init__(self, coeff, tile, floor=False):
        surf = resources.surface.get(tile)
        self.surf_w = surf.get_width()

        display = self.program.window.display

        super().__init__(
            resources.surface.new((display.width + self.surf_w, surf.get_height()))
        )

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


class Bush(BatchTile):
    def __init__(self):
        super().__init__(state.config.bush_parallax_coeff, Graphics.BG_BUSH)


class City(BatchTile):
    def __init__(self):
        super().__init__(state.config.city_parallax_coeff, Graphics.BG_CITY)


class Clouds(BatchTile):
    def __init__(self):
        super().__init__(state.config.clouds_parallax_coeff, Graphics.BG_CLOUDS)


class Floor(BatchTile):
    def __init__(self):
        super().__init__(state.config.floor_parallax_coeff, Graphics.FLOOR, True)
