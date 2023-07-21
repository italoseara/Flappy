import enum
import random

import state
from constants import GameMode, Graphics
from gameengine import resources
from gameengine.basenode import BaseNode
from gameengine.graphicnode import GraphicNode


class Pipe(GraphicNode):
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


class PipeSet(BaseNode):
    def __init__(self):
        self.top = Pipe(Pipe.TOP)
        self.bot = Pipe(Pipe.BOT)

        super().__init__(self.top, self.bot)

        self.top.rect.y = random.randint(*state.pipe_y_offset_range)
        self.bot.rect.y = self.top.rect.bottom + state.pipe_y_spacing

        self.rect = self.top.rect.copy()
        self.rect.height *= 2
        self.rect.height + state.pipe_y_spacing

        self.incresead = False

    def update(self):
        super().update()

        self.rect.x = self.top.rect.x

        player = self.program.scene.game.player

        if player.hitbox.rect.colliderect(self.rect):
            if player.hitbox.rect.collidelist((self.top.rect, self.bot.rect)) != -1:
                player.die()
            elif player.hitbox.rect.right >= self.rect.right and not self.incresead:
                self.incresead = True
                self.program.scene.score.increase()


class Pipes(BaseNode):
    def generate_pipes(self):
        self.add_children(PipeSet())

    def update(self):
        if state.game_mode == GameMode.PLAYING and not state.is_paused:
            if (
                len(self.children) == 0
                or self.children[-1].top.rect.x - self.program.window.display.width
                <= -state.pipe_x_spacing
            ):
                self.generate_pipes()

            super().update()
