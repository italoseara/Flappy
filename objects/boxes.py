from constants import Graphics
from gameengine import resources
from gameengine.graphicnode import GraphicNode


class BoxEnd(GraphicNode):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.BOX_END))
        self.rect.x = 258
        self.rect.y = 145
