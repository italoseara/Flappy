from constants import GameMode, Graphics
from new_gameengine.basechild import BaseChild
from new_gameengine import resources
from gamestate import GameState


class MsgReady(BaseChild):
    def __init__(self, program):
        super().__init__(program, resources.surface.get(Graphics.MSG_READY))
        self.rect.x = 222
        self.rect.y = 20

    def update(self):
        self.active = GameState.game_mode == GameMode.START

        super().update()
