from gameengine.display import Display
from gameengine.hierarchicalobject import HierarchicalObject


class BaseScene(HierarchicalObject):
    bg = (0, 0, 0)
    focus = None

    def __init__(self):
        super().__init__()
        self.surface = Display.surface
        self.parent = self
        self.children = []

    def set_focus(self, obj, update_priority=True):
        if obj in self.children:
            self.focus = obj
            if update_priority:
                self.children.append(self.children.pop(self.children.index(obj)))

    def update(self, *args, **kwargs):
        # update reference to display surface
        self.surface = Display.surface

        super().update(*args, **kwargs)
        self.update_focus()

    def update_focus(self, *args, **kwargs):
        if self.focus is not None:
            self.focus.update_focus()

    def draw(self):
        self.surface.fill(self.bg)
        super().draw()
