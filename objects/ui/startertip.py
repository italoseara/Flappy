import state
from constants import GameMode, Graphics
from gameengine import resources
from gameengine.basechild import BaseChild


class StarterTip(BaseChild):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.STARTER_TIP))
        self.rect.x = 450
        self.rect.y = 200

    def update(self):
        self.active = state.game_mode == GameMode.START

        super().update()
