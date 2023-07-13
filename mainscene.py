from gameengine.basescene import BaseScene
from gameengine.engine import Engine
from objects.bird import Bird


class MainScene(BaseScene):
    def __init__(self):
        super().__init__()

        self.bg = (11, 200, 215)

        self.add_children(Bird())

    def update(self):
        super().update()

        if Engine.request_quit:
            Engine.system_exit()
