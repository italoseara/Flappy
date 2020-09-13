from core.maths import Vector2
from core.data import FrameManager
from core.render import BatchRender
        
class ScrollingTileH(BatchRender):
    def __init__(self, pos_y, resource, speed, win_size):
        self.pos = Vector2(0, pos_y)
        self.frames = FrameManager([resource])

        self.speed = speed
        self._win_size = win_size

    def process(self):
        self.pos.x += self.speed
        self.pos.x %= self.frames.current_frame.size.x

    def get_render(self):
        result = []

        i = -1
        root = int(self.pos.x)
        tile_size_x = self.frames.current_frame.size.x
        while root + i * tile_size_x < self._win_size.x:
            result.append((
                self.frames.current_frame,
                (root + i * tile_size_x, self.pos.y)
            ))
            i += 1

        return result

