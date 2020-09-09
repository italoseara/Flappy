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
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], tuple) and len(args[0]) == 2:
            self.x, self.y = args[0]
        elif len(args) == 2:
            self.x, self.y = args
        else:
            raise TypeError("could not find matching pattern for argument list: {}{}".format(
                type(self),
                args,
            ))

    def into_tuple(self) -> tuple:
        return (self.x, self.y)
