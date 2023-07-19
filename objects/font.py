import pygame

import state
from constants import GameMode, Sounds
from gameengine import resources
from gameengine.basechild import BaseChild
from gameengine.hierarchicalobject import HierarchicalObject


class Digit(BaseChild):
    def __init__(self, digit, col_offset, index, font):
        super().__init__(font.font_dict[digit])
        self.digit = digit
        self.column_offset = col_offset
        self.font = font
        self.index = index
        self.update_pos()

    def update(self):
        super().update()
        self.update_pos()

    def update_pos(self):
        self.rect.x = (
            self.font.rect.x + self.column_offset + (self.index * self.font.padding_px)
        )
        self.rect.y = self.font.rect.y + self.font.padding_px


class SpriteFont(HierarchicalObject):
    def __init__(self, font_dict, padding_px, scale=1):
        super().__init__()
        self.rect = pygame.FRect(0, 0, 0, 0)
        self.font_dict = font_dict
        self.padding_px = padding_px
        self.scale = scale
        self.text = ""

    def update(self):
        super().update()

    def update_size(self):
        if len(self.children) > 0:
            max_w = (
                sum([d.rect.w + self.padding_px for d in self.children])
                + self.padding_px
            )
            max_h = self.children[0].rect.h + 2 * self.padding_px
            self.rect.size = (max_w, max_h)

    def set_text(self, text):
        self.children.clear()
        self.text = str(text)

        col = 0
        for index, digit in enumerate(self.text):
            self.add_children(Digit(digit, col, index, self))
            col += self.font_dict[digit].get_width()
        self.update_size()


class ScoreLabel(SpriteFont):
    @property
    def score(self):
        return int(self.text)


class BigFontScore(ScoreLabel):
    def __init__(self, font_dict, padding_px, scale=1):
        super().__init__(font_dict, padding_px, scale)

        self.set_text("0")
        self.visible = False

    def increase_score(self):
        self.set_text(self.score + 1)
        pygame.mixer.Channel(1).play(resources.sound.get(Sounds.POINT))

    def update(self):
        self.visible = state.game_mode == GameMode.PLAYING
        if self.visible:
            self.rect.y = 15
            self.rect.centerx = self.program.window.display.rect.centerx
            super().update()
