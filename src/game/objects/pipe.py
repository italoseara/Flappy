from core.entity import Entity

class Pipe(Entity):
    def __init__(self, pos, frames, speed=-1.0):
        self.setup(pos, frames)
        self.speed = speed

        # used in the main code to check if the player has gotten the score from this pipe already.
        self.has_scored = False

    def process(self):
        self.pos.x += self.speed
