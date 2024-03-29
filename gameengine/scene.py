from .basenode import BaseNode


class BaseScene(BaseNode):
    bg = (0, 0, 0)

    def __init__(self):
        super().__init__()
        self.parent = self.program.window.display

    def draw(self):
        self.surface.fill(self.bg)
        super().draw()
