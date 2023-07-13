from constants import Graphics
from gameengine.animation import Animation
from gameengine.basechild import BaseChild
from gameengine.display import Display
from gameengine.resources import Resources


class PauseButton(BaseChild):
    def __init__(self):
        super().__init__(
            Animation.from_assets(
                None,
                Resources.Surface.get(Graphics.BTN_PAUSE_NORMAL),
                Resources.Surface.get(Graphics.BTN_PAUSE_PAUSED),
            )
        )

        self.rect.right = Display.width - 10
        self.rect.y = 10
