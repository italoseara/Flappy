from core.maths import image_size
from core.entity import Entity
        
class ScrollingTile(Entity):
    def __init__(self, pos, resource, speed, wrap_pos):
        super().__init__(pos, [resource])
        self.speed = speed
        self.wrap_pos = wrap_pos
        self._size_x = image_size(self.frames.frame_list[0])[0]

    def process(self):
        self.pos.x += self.speed

        if self.pos.x <= 0 - self._size_x:
            self.pos.x += self.wrap_pos + self._size_x
            
        
