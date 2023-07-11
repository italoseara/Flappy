from gameengine.basescene import BaseScene
from gameengine.engine import Engine


class MainScene(BaseScene):
    def __init__(self):
        super().__init__()

        self.bg = (11, 200, 215)

    def update(self):
        super().update()

        if Engine.request_quit:
            Engine.system_exit()
