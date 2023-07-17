from .hierarchicalobject import HierarchicalObject


class BaseScene(HierarchicalObject):
    bg = (0, 0, 0)

    def __init__(self, program):
        super().__init__(program)
        self.parent = self
        self.program = program
        self.surface = program.window.display.surface

    def draw(self):
        self.surface.fill(self.bg)
        super().draw()
