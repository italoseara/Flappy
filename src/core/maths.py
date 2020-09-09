from __future__ import annotations
from pygame import Rect

def image_size(image) -> tuple:
    """Obtains the size of an image."""
    return image.get_rect().size

def image_rectangle(image) -> tuple:
    """Obtains the rectangle of an image."""
    return Rect((0, 0) + image_size(image))

def gameobject_size(gameobject) -> tuple:
    """Obtains the size of an entity/gameobject."""
    return image_size(gameobject.frames.current_frame)

def gameobject_hitbox(gameobject) -> tuple:
    """Obtains the hitbox rectangle of an image."""
    return Rect(gameobject.pos.into_tuple() + image_size(gameobject.frames.current_frame))

def gameobject_render(gameobject, screen) -> None:
    raise Exception("deprecated function")
    # """Renders an object."""
    # render_result = gameobject.render()
    # if isinstance(render_result, list):
    #     for r in render_result:
    #         screen.blit(*r)
    # else:
    #     screen.blit(*render_result)

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_tuple(tup) -> Vector2:
        e1, e2 = tup
        return Vector2(e1, e2)

    def into_tuple(self) -> tuple:
        return (self.x, self.y)
