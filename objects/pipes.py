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
    def __init__(self):
        super().__init__()

        self.aligned_to_bird = []
        self.bird_inside = False
        self.last_pipe = None

    def update(self):
        if not (state.is_paused or state.game_mode == GameMode.DEAD):
            super().update()
            self.check_bird_collision()

            if len(self.children) == 0:
                if state.game_mode == GameMode.PLAYING:
                    self.generate_pipe()
            elif (
                self.children[-1].rect.x - self.program.window.display.width
            ) <= -state.pipe_x_spacing:
                self.generate_pipe()

    def check_bird_collision(self):
        self.aligned_to_bird.clear()
        for i in range(0, len(self.children), 2):
            pair_pipe_rect = (next_last_pipe := self.children[i]).hitbox.rect.copy()
            pair_pipe_rect.y = 0
            pair_pipe_rect.height = self.program.window.display.height

            self.program.scene.bird.check_in_between_pipes(pair_pipe_rect)

            if self.program.scene.bird.between_pipes:
                self.aligned_to_bird = [self.children[i], self.children[i + 1]]
                if self.last_pipe not in self.aligned_to_bird:
                    if self.check_point(pair_pipe_rect):
                        self.last_pipe = next_last_pipe
                break

    def check_point(self, pair_pipe_rect):
        if self.program.scene.bird.hitbox.rect.right > pair_pipe_rect.right:
            self.program.scene.big_font.increase_score()
            return True
        return False

    def generate_pipe(self):
        top = Pipe(Pipe.TOP)
        bot = Pipe(Pipe.BOT)
        self.add_children(top, bot)

        top.rect.bottom = random.randint(*state.pipe_y_offset_range) + top.rect.height
        bot.rect.top = top.rect.bottom + state.pipe_y_spacing
