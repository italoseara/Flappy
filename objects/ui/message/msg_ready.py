import state
from constants import GameMode, Graphics
from gameengine import resources
from gameengine.basechild import BaseChild


class MsgReady(BaseChild):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.MSG_READY))
        self.rect.x = 222
        self.rect.y = 20

    def update(self):
        self.active = state.game_mode == GameMode.START

        super().update()
