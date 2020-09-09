import random

from pygame import Rect
from core.render import BatchRender
from core.maths import image_size, Vector2
from core.data import FrameManager

class TBPipes(BatchRender):
    def __init__(self,
                 win_size, resources, speed,
                 x_offset, y_offset_range, y_spacing):
        self.speed = speed
        self._win_size = win_size
        self.x_offset = x_offset,
        self.y_offset_range = y_offset_range
        self.y_spacing = y_spacing

        self._size_x = image_size(resources[0])[0]
        self._size_y = image_size(resources[0])[1]

        self.current_y_offset = 0 # initial, before calculation

        self.pos = Vector2(
            win_size[0] + x_offset,
            self.get_y_pos(),
        )
        self.frames = FrameManager(resources)

        # calculate pipes
        self._calculated_pipes = None
        self.calc_pipes()

    def process(self):
        self.pos.x += self.speed

        # if the pipe has passed entirely through the left size of the screen
        if self.pos.x < -self._size_x:
            self.pos.x += self._win_size[0] + self._size_x
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
                Rect((self.pos.x,
                      self.pos.y + i * (self._size_y + self.y_spacing)),
                     image_size(self.frames.frame_list[i]))
            ) for i in [0, 1]
        ]

    def get_render(self):
        return self._calculated_pipes

