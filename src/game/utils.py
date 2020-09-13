import pygame
from typing import List, Tuple, Dict, Any

def dict_from_pairs(pairs: List[Tuple[Any, Any]]) -> Dict[Any, Any]:
    result = {}
    for (k, v) in pairs:
        result[k] = v
    return result

def amount_to_fill_container(container_size, object_size):
    """Calculates the minimum amount of objects (size `object_size`) needed
    to fill the container (size `container_size`).

    The returned amount might not fit inside the container - in this case,
    it will be one more than what would fit.
    """
    result = container_size / object_size
    if result % 1 > 0:
        result += (1 - result % 1)
    return int(result)

def make_color(arg):
    if isinstance(arg, tuple):
        return pygame.Color(*arg)
    return pygame.Color(arg)
