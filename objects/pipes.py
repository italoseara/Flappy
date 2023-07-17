import enum
import random

import state
from constants import GameMode, Graphics
from gameengine import resources
from gameengine.basechild import BaseChild
from gameengine.hierarchicalobject import HierarchicalObject


class Pipe(BaseChild):
    TOP = enum.auto()
    BOT = enum.auto()

    surfaces = {
        TOP: Graphics.PIPE_TOP,
        BOT: Graphics.PIPE_BOT,
    }

    def __init__(self, pipe_type):
        super().__init__(resources.surface.get(self.surfaces[pipe_type]))

        self.rect.x = self.program.window.display.width

        self.speed = -state.config.scroll_speed

    def update(self):
        super().update()

        self.rect.x += self.speed * self.program.time.delta

        if self.rect.right <= 0:
            self.kill()


class PipeGenerator(HierarchicalObject):
    def update(self):
        if not (state.is_paused or state.game_mode == GameMode.DEAD):
            super().update()
            if len(self.children) == 0:
                if state.game_mode == GameMode.PLAYING:
                    self.generate_pipe()
            elif (
                self.children[-1].rect.right - self.program.window.display.width
            ) <= -state.pipe_x_spacing:
                self.generate_pipe()

    @property
    def surface(self):
        return self.parent.surface

    def generate_pipe(self):
        top = Pipe(Pipe.TOP)
        bot = Pipe(Pipe.BOT)
        self.add_children(top, bot)

        top.rect.bottom = random.randint(*state.pipe_y_offset_range) + top.rect.height
        bot.rect.top = top.rect.bottom + state.pipe_y_spacing
