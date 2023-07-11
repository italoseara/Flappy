from .hierarchicalobject import HierarchicalObject


class BaseChild(HierarchicalObject):
    surface = None
    rect = None
    bg = None

    def update_focus(self):
        pass

    def draw(self):
        if self.bg is not None:
            self.surface.fill(self.bg)

        super().draw()

        self.parent.surface.blit(self.surface, self.rect)
