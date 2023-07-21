import state
from constants import GameMode
from gameengine.basenode import BaseNode
from gameengine.timer import Timer
from objects.boxes import BoxEnd
from objects.buttons import BtnPlay, BtnScoreboard
from objects.labels import ScoreLabel
from objects.others import Medal


class Ending(BaseNode):
    def __init__(self):
        super().__init__()

        self.small_font = ScoreLabel(type=ScoreLabel.SMALL, padding=2)
        self.max_small_font = ScoreLabel(type=ScoreLabel.SMALL, padding=2)
        self.timer = Timer(1.12)
        self.add_children(
            self.timer,
            BoxEnd(),
            BtnPlay(),
            BtnScoreboard(),
            Medal(),
            self.max_small_font,
            self.small_font,
        )

        self.active = False

    def update(self):
        if state.game_mode == GameMode.DEAD:
            super().update()
            if self.timer.reached:
                score = self.program.scene.score
                score.register(score.current_score_value)

                self.small_font.set_text(score.current_score_value)
                self.small_font.rect.right = 660
                self.small_font.rect.bottom = 235

                self.max_small_font.set_text(max(score.registered))
                self.max_small_font.rect.right = 660
                self.max_small_font.rect.bottom = 320
                self.active = True

                self.timer.rechead = 0
