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
    return Rect(gameobject.pos.to_tuple() + image_size(gameobject.frames.current_frame))

def gameobject_render(gameobject, screen) -> None:
    """Renders an object."""
    screen.blit(*gameobject.render())

