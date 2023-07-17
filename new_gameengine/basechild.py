import pygame

from new_gameengine.animation import Animation

from .hierarchicalobject import HierarchicalObject


class HitBox:
    def __init__(self, child, rect):
        self.update(child, rect)

    def update(self, surface, rect):
        self.rect = surface.get_bounding_rect()
        self.rect.x += rect.x
        self.rect.y += rect.y


class Rotation:
    def __init__(self):
        self.angle = 0

    def update(self, target):
        if self.angle != 0:
            target.surface = pygame.transform.rotate(target.surface, self.angle)


class BaseChild(HierarchicalObject):
    surface = None
    rect = None
    offset = None
    bg = None

    hitbox = None
    animation = None
    rotation = None

    active = None
    visible = None

    def __init__(self, program, image):
        HierarchicalObject.__init__(self, program)

        if type(image) is Animation:
            self.animation = image
            self.surface = image.current_frame
        else:
            self.surface = image
        self.rect = self.surface.get_frect()
        self.offset = pygame.Vector2(0, 0)
        self.hitbox = HitBox(self.surface, self.rect)
        self.rotation = Rotation()

        self.visible = True
        self.active = True

    def update_focus(self):
        pass

    def update(self):
        if self.active:
            if self.animation is not None:
                self.animation.update(self)
                self.surface = self.animation.current_frame
            self.rotation.update(self)
            HierarchicalObject.update(self)

    def draw(self):
        if self.active and self.visible:
            self.hitbox.update(self.surface, self.rect)
            if self.bg is not None:
                self.surface.fill(self.bg)

            HierarchicalObject.draw(self)

            self.parent.surface.blit(
                self.surface,
                (self.rect.x + self.offset.x, self.rect.y + self.offset.y),
            )
