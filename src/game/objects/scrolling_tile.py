from core.entity import SimpleEntity
        
class ScrollingTile(SimpleEntity):
    def __init__(self, pos, resource, speed, wrap_pos):
        super().__init__(pos, [resource])
        self.speed = speed
        self.wrap_pos = wrap_pos
        self._size_x = self.frames.frame_list[0].size.x

    def process(self):
        self.pos.x += self.speed

        if self.pos.x <= 0 - self._size_x:
            self.pos.x += self.wrap_pos + self._size_x
            
        
