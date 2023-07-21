import state
from constants import GameMode, Graphics
from gameengine import resources
from gameengine.graphicnode import GraphicNode


class MsgGameOver(GraphicNode):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.MSG_GAME_OVER))
        self.rect.x = 222
        self.rect.y = 20


class MsgReady(GraphicNode):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.MSG_READY))
        self.rect.x = 222
        self.rect.y = 20

    def update(self):
        self.visible = state.game_mode == GameMode.START
