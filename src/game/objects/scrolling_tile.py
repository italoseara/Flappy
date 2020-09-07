from core.entity import Entity
        
class ScrollingTile(Entity):
    def __init__(self, pos, resource, speed=-1.0, parallax_coeff=1.0):
        super().__init__(pos, [resource])
        self.speed = float(speed)
        self.parallax_coeff = float(parallax_coeff)

    def process(self):
        self.pos.x += self.speed
