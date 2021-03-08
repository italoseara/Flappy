from core.maths import Vector2
from core.data import FrameManager
from core.render import BatchRender
from core.time import DeltaTime

class ScrollingTileH(BatchRender):
    def __init__(self, pos_y, resource, speed, win_size):
        self.pos = Vector2(0, pos_y)
        self.frames = FrameManager([resource])

        self.speed = speed
        self._win_size = Vector2(win_size)

    def process(self):
        self.pos.x = ((self.pos.x + self.speed) % self.frames.current_frame.size.x) * DeltaTime.get()

    def get_render(self):
        result = []

        tile_size_x = self.frames.current_frame.size.x
        pos_x = -tile_size_x + self.pos.x
        while pos_x < self._win_size.x:
            result.append((
                self.frames.current_frame,
                (pos_x, self.pos.y)
            ))
            pos_x += tile_size_x

        return result
