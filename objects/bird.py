from constants import Graphics
from gameengine.animation import Animation
from gameengine.basechild import BaseChild
from gameengine.resources import Resources


class Bird(BaseChild):
    def __init__(self):
        super().__init__(
            Animation.from_assets(
                5,
                Resources.Surface.get(Graphics.BIRD_F0),
                Resources.Surface.get(Graphics.BIRD_F1),
            )
        )
        
