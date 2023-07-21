import enum

import state
from constants import GameMode, Graphics
from gameengine import resources
from objects.font import SpriteFont


class ScoreLabel(SpriteFont):
    SMALL = enum.auto()
    BIG = enum.auto()

    def __init__(self, type, padding):
        if type is ScoreLabel.BIG:
            char_set = "CHAR_B"
        elif type is ScoreLabel.SMALL:
            char_set = "CHAR_S"
        super().__init__(
            font_dict={
                str(i): resources.surface.get(Graphics.__dict__[f"{char_set}{i}"])
                for i in range(10)
            },
            padding_px=padding,
        )


class BigScoreLabel(ScoreLabel):
    def __init__(self):
        super().__init__(type=ScoreLabel.BIG, padding=3)

        self.set_text(0)
        self.visible = False

    def update(self):
        self.visible = state.game_mode == GameMode.PLAYING
        if self.visible:
            self.set_text(self.program.scene.score.current_score_value)

            self.rect.y = 15
            self.rect.centerx = self.program.window.display.rect.centerx
            super().update()
