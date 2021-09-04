from core.maths import Vector2
from core.data import FrameManager, Blittable
from core.render import BatchRender
from typing import List, Tuple

class ScrollingTileH(BatchRender):
    def __init__(self, pos_y, resource, speed, win_size: Vector2):
        self.pos = Vector2(0, pos_y)
        self.frames = FrameManager([resource])

        self.speed = speed
        self._win_size = win_size

    def process(self, state):
        self.pos.x = ((self.pos.x + self.speed * state.delta_time) % self.frames.current_frame.size.x)

    def get_render(self) -> List[Tuple[Blittable, Vector2]]:
        result = []

        tile_size_x = self.frames.current_frame.size.x
        pos_x = -tile_size_x + self.pos.x
        while pos_x < self._win_size.x:
            result.append((
                self.frames.current_frame,
                Vector2(pos_x, self.pos.y)
            ))
            pos_x += tile_size_x

        return result
