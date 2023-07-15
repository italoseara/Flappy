import pygame

from .animation import Animation
from .hierarchicalobject import HierarchicalObject


class TransformedChild:
    def __init__(self):
        self.rotation = self.Rotation()

    def update(self, surface):
        return self.rotation.update(surface)

    class Rotation:
        def __init__(self):
            self.angle = 0

        def update(self, surface):
            if self.angle != 0:
                return pygame.transform.rotate(surface, self.angle)
            return surface


class AnimatedChild:
    has_animation = False

    def __init__(self, image):
        self.__check_animation(image)

    def __check_animation(self, image):
        self.has_animation = type(image) == Animation

    def _get_surface(self, image):
        return image.current_frame if self.has_animation else image

    def update(self, image):
        self.__check_animation(image)
        if self.has_animation:
            image.update()


class BaseChild(HierarchicalObject, AnimatedChild, TransformedChild):
    image = None
    surface = None
    rect = None
    offset = None
    bg = None
    
    active = None
    visible = None

    def __init__(self, image):
        HierarchicalObject.__init__(self)
        AnimatedChild.__init__(self, image)
        TransformedChild.__init__(self)

        self.image = image
        self.surface = AnimatedChild._get_surface(self, image)
        self.rect = self.surface.get_frect()
        self.offset = pygame.Vector2(0, 0)
        
        self.visible = True
        self.active = True

    def update_focus(self):
        pass

    def update(self):
        if self.active:
            AnimatedChild.update(self, self.image)
            self.surface = AnimatedChild._get_surface(self, self.image)
            self.surface = TransformedChild.update(self, self.surface)

            self.rect.size = self.surface.get_size()

            HierarchicalObject.update(self)

    def draw(self):
        if self.active:
            if self.active:
                if self.bg is not None:
                    self.image.fill(self.bg)

                HierarchicalObject.draw(self)

                self.parent.surface.blit(
                    self.surface, (self.rect.x - self.offset.x, self.rect.y - self.offset.y)
                )
