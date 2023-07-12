from .hierarchicalobject import HierarchicalObject


class BaseChild(HierarchicalObject):
    surface = None
    rect = None
    bg = None

    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.rect = surface.get_frect()

    def update_focus(self):
        pass

    def draw(self):
        if self.bg is not None:
            self.surface.fill(self.bg)

        super().draw()

        self.parent.surface.blit(self.surface, self.rect)
