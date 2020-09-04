from core.entity import Entity

class Pipe(Entity):
    def __init__(self, pos, frames, speed=-1.0):
        self.setup(pos, frames)
        self.speed = speed

        # Usado no código principal para ver se o jogador já passou desse cano e já pegou a pontuação.
        self.has_scored = False

    def process(self):
        self.pos.x += self.speed
