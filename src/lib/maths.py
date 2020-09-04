from pygame import Rect

def image_size(image) -> tuple:
    """Obtém o tamanho de uma imagem."""
    return image.get_rect().size

def image_rectangle(image) -> tuple:
    """Obtém o retângulo de uma imagem."""
    return Rect((0, 0) + image_size(image))

def gameobject_size(gameobject) -> tuple:
    """Obtém o tamanho de um Object."""
    return image_size(gameobject.frames.current_frame)

def gameobject_hitbox(gameobject) -> tuple:
    """Obtém um retângulo de um Object com tamanho da sua imagem e sua posição."""
    return Rect(gameobject.pos.to_tuple() + image_size(gameobject.frames.current_frame))

def gameobject_render(gameobject, screen) -> None:
    """Renderiza um Object."""
    screen.blit(*gameobject.render())

