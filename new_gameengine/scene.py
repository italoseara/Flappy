from .hierarchicalobject import HierarchicalObject


class BaseScene(HierarchicalObject):
    bg = (0, 0, 0)

    def __init__(self):
        super().__init__()
        self.parent = self
        self.surface = self.program.window.display.surface

    def draw(self):
        self.surface.fill(self.bg)
        super().draw()
