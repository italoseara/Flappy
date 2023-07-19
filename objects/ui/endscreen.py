import pygame

import state
from constants import GameMode, Graphics
from gameengine import resources
from gameengine.basechild import BaseChild
from gameengine.hierarchicalobject import HierarchicalObject
from gameengine.timer import Timer
from objects.font import ScoreLabel


class MsgGameOver(BaseChild):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.MSG_GAME_OVER))
        self.rect.x = 222
        self.rect.y = 20


class BoxEnd(BaseChild):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.BOX_END))
        self.rect.x = 258
        self.rect.y = 145


class ButtonPlay(BaseChild):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.BTN_PLAY))
        self.rect.x = 280
        self.rect.y = 405

    def update(self):
        super().update()

        if self.hitbox.rect.collidepoint(
            self.program.devices.mouse.pos
        ) and self.program.devices.mouse.get_pressed_in_frame(pygame.BUTTON_LEFT):
            self.program.scene.reset()


class ButtonScoreboard(BaseChild):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.BTN_SCOREBOARD))
        self.rect.x = 520
        self.rect.y = 405


class Medal(BaseChild):
    def __init__(self):
        self.default_surface = resources.surface.new((88, 88))

        super().__init__(self.default_surface)
        self.rect.x = 308
        self.rect.y = 225

    def update(self):
        super().update()

        if self.surface is self.default_surface:
            if (score := self.program.scene.big_font.score) >= 60:
                self.surface = resources.surface.get(Graphics.MEDAL_GOLD)
            elif score >= 30:
                self.surface = resources.surface.get(Graphics.MEDAL_SILVER)
            elif score >= 15:
                self.surface = resources.surface.get(Graphics.MEDAL_BRONZE)


class EndScreen(HierarchicalObject):
    def __init__(self):
        super().__init__()

        self.small_font = ScoreLabel(
            font_dict={
                str(i): resources.surface.get(Graphics.__dict__[f"CHAR_S{i}"])
                for i in range(10)
            },
            padding_px=2,
        )
        self.max_small_font = ScoreLabel(
            font_dict={
                str(i): resources.surface.get(Graphics.__dict__[f"CHAR_S{i}"])
                for i in range(10)
            },
            padding_px=2,
        )
        self.timer = Timer(1.12)
        self.add_children(
            self.timer,
            MsgGameOver(),
            BoxEnd(),
            ButtonPlay(),
            ButtonScoreboard(),
            Medal(),
            self.small_font,
            self.max_small_font,
        )

        self.active = False

    def update(self):
        if state.game_mode == GameMode.DEAD:
            super().update()
            if self.timer.reached:
                self.small_font.set_text(score := self.program.scene.big_font.text)
                self.small_font.rect.right = 660
                self.small_font.rect.bottom = 235

                self.max_small_font.set_text(score)
                self.max_small_font.rect.right = 660
                self.max_small_font.rect.bottom = 320
                self.active = True
