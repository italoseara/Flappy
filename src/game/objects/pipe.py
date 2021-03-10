import random

from pygame import Rect
from core.render import BatchRender
from core.maths import Vector2
from core.data import FrameManager
from core.time import DeltaTime

class TBPipes(BatchRender):
    def __init__(self,
                 win_size, resources, speed,
                 x_offset, y_offset_range, y_spacing):
        self.speed = speed
        self._win_size = tuple(win_size)
        self.x_offset = x_offset,
        self.y_offset_range = y_offset_range
        self.y_spacing = y_spacing

        self._size = resources[0].size

        self.current_y_offset = 0 # initial, before calculation

        self.pos = Vector2(
            self._win_size[0] + x_offset,
            self.get_y_pos(),
        )
        self.frames = FrameManager(resources)

        # calculate pipes
        self._calculated_pipes = None
        self.calc_pipes()

    def process(self, deltatime):
        self.pos.x += self.speed * deltatime.get()

        # if the pipe has passed entirely through the left size of the screen
        if self.pos.x < -self._size.x:
            self.pos.x += self._win_size[0] + self._size.x
            self.current_y_offset = self.get_y_pos()

        self.calc_pipes()

    def get_y_pos(self):
        return random.randint(*self.y_offset_range)

    def is_colliding(self, other):
        for pipe in self._calculated_pipes:
            if pipe[1].colliderect(other):
                return True
        return False

    def get_hitboxes(self):
        return [x[1] for x in self._calculated_pipes]

    def calc_pipes(self):
        self._calculated_pipes = [
            (
                self.frames.frame_list[i],
                Rect(
                    (self.pos.x, self.pos.y + i * (self._size.y + self.y_spacing)),
                    tuple(self.frames.frame_list[i].size),
                ),
            ) for i in [0, 1]
        ]

    def get_render(self):
        return self._calculated_pipes

