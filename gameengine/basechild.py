from .animation import Animation
from .hierarchicalobject import HierarchicalObject


class AnimatedChild:
    has_animation = False

    def __init__(self, surface):
        self.__check_animation(surface)

    def __check_animation(self, surface):
        self.has_animation = type(surface) == Animation

    def _get_current_rect(self, surface):
        surf = surface.current_frame if self.has_animation else surface
        return surf.get_frect()

    def update(self, surface, rect):
        self.__check_animation(surface)
        if self.has_animation:
            surface.update()
            rect.size = self._get_current_rect(surface).size

    def draw(self, parent, surface, rect):
        surf = surface.current_frame if self.has_animation else surface
        parent.surface.blit(surf, rect)


class BaseChild(HierarchicalObject, AnimatedChild):
    surface = None
    rect = None
    bg = None

    def __init__(self, surface):
        HierarchicalObject.__init__(self)
        AnimatedChild.__init__(self, surface)

        self.surface = surface
        self.rect = self._get_current_rect(surface)

    def update_focus(self):
        pass

    def update(self):
        AnimatedChild.update(self, self.surface, self.rect)
        HierarchicalObject.update(self)

    def draw(self):
        if self.bg is not None:
            self.surface.fill(self.bg)

        HierarchicalObject.draw(self)
        AnimatedChild.draw(self, self.parent, self.surface, self.rect)
