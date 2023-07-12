from constants import Graphics
from gameengine.basechild import BaseChild
from gameengine.resources import Resources


class Bird(BaseChild):
    def __init__(self):
        super().__init__(Resources.Surface.get(Graphics.BIRD_F0))
