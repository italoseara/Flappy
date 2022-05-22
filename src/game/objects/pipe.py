import random

from pygame import Rect
from core.render import BatchRender
from core.maths import Vector2
from core.data import FrameManager, Blittable
from typing import List, Tuple

class TBPipes(BatchRender):
    def __init__(self, win_size: Vector2, resources, speed, x_offset, y_offset_range, y_spacing):
        self.speed = speed
        self._win_size = win_size
        self.x_offset = x_offset,
        self.y_offset_range = y_offset_range
        self.y_spacing = y_spacing

        self.size = resources[0].size

        self.current_y_offset = 0 # initial, before calculation

        self.pos = Vector2(
            self._win_size.x + x_offset,
            self.get_y_pos(),
        )
        self.frames = FrameManager(resources)

        # calculate pipes
        self._calculated_pipes = self.calc_pipes()

    def process(self, state):
        self.pos.x += self.speed * state.delta_time

        # if the pipe has passed entirely through the left size of the screen
        if self.pos.x < -self.size.x:
            self.pos.x += self._win_size.x + self.size.x
            self.current_y_offset = self.get_y_pos()

        self._calculated_pipes = self.calc_pipes()

    def get_y_pos(self, multiple=20):
        return random.randint(*self.y_offset_range)//multiple*multiple

    def is_colliding(self, other):
        for pipe in self._calculated_pipes:
            if pipe[1].colliderect(other):
                return True
        return False

    def get_hitboxes(self):
        return [x[1] for x in self._calculated_pipes]

    def calc_pipes(self) -> List[Tuple[Blittable, Rect]]:
        return [(
            self.frames.frame_list[i],
            Rect(
                (self.pos.x, self.pos.y + i * (self.size.y + self.y_spacing)),
                self.frames.frame_list[i].size.to_tuple(),
            ),
        ) for i in [0, 1]]

    def get_render(self) -> List[Tuple[Blittable, Vector2]]:
        return [(blt, Vector2(rect.x, rect.y)) for (blt, rect) in self._calculated_pipes]
