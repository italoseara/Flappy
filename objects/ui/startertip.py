from constants import GameMode, Graphics
from gameengine import resources
from gameengine.basechild import BaseChild
from gamestate import GameState


class StarterTip(BaseChild):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.STARTER_TIP))
        self.rect.x = 450
        self.rect.y = 200

    def update(self):
        self.active = GameState.game_mode == GameMode.START

        super().update()
