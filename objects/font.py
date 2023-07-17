import pygame
from constants import GameMode

from gameengine.basechild import BaseChild
from gameengine.hierarchicalobject import HierarchicalObject
import state


class Digit(BaseChild):
    def __init__(self, digit, col, index, font):
        super().__init__(font.font_dict[digit])
        self.digit = digit
        self.column = col
        self.font = font
        self.index = index
        self.update_pos()
        
    def update_pos(self):
        self.rect.x = self.font.rect.x + self.column + ( self.index * self.font.padding_px )
        self.rect.y = self.font.rect.y + self.font.padding_px


class SpriteFont(HierarchicalObject):
    def __init__(self, font_dict, padding_px, scale=1):
        super().__init__()
        self.rect = pygame.FRect(0,0,0,0)
        self.font_dict = font_dict
        self.padding_px = padding_px
        self.scale = scale
        self.text = ''

    @property
    def surface(self): return self.parent.surface

    @property
    def visible(self):
        return self.children[0].visible

    @visible.setter
    def visible(self, value): 
        for d in self.children:
            d.visible = value

    def set_pos(self, new_pos):
        self.rect.topleft = new_pos
        self.update_pos()
        
    def update_pos(self):
        for d in self.children:
            d.update_pos()
                
    def update_size(self):
        if len(self.children) > 0:
            max_w = max([d.rect.right-self.rect.right for d in self.children])
            max_h = max([d.rect.bottom-self.rect.bottom for d in self.children])
            self.rect.size = (max_w, max_h)


    def set_text(self, text):
        self.children.clear()
        self.text = str(text)
        
        col = 0
        for index, digit in enumerate(self.text):
            self.add_children(Digit(digit, col, index, self))
            col += self.font_dict[digit].get_width()
        self.update_size()
            


class BigFont(SpriteFont):
    def update(self):
        super().update()
        self.visible = state.game_mode == GameMode.PLAYING
    
    def set_text(self, text):
        super().set_text(text)
        self.update_default_pos()
    
    def update_default_pos(self):
        self.set_pos((self.program.window.display.rect.w/2-self.rect.w/2, 17))
        super().update_pos()