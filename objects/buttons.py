import pygame

import state
from constants import GameMode, Graphics
from gameengine import resources
from gameengine.graphicnode import GraphicNode


class BtnPause(GraphicNode):
    def __init__(self):
        self.surf_normal = resources.surface.get(Graphics.BTN_PAUSE_NORMAL)
        self.surf_paused = resources.surface.get(Graphics.BTN_PAUSE_PAUSED)
        super().__init__(self.surf_normal)

        self.rect.right = self.program.window.display.width - 10
        self.rect.y = 10

        self.pressed = False

    def update(self):
        self.visible = state.game_mode == GameMode.PLAYING
        if self.visible:
            self.pressed = (
                self.rect.collidepoint(self.program.devices.mouse.pos)
                and self.program.devices.mouse.get_pressed_in_frame(pygame.BUTTON_LEFT)
            ) or self.program.devices.keyboard.get_pressed_in_frame(
                pygame.KEYDOWN, pygame.K_ESCAPE
            )

            if self.pressed and state.game_mode != GameMode.DEAD:
                state.is_paused = not state.is_paused

            self.surface = self.surf_paused if state.is_paused else self.surf_normal


class BtnPlay(GraphicNode):
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


class BtnScoreboard(GraphicNode):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.BTN_SCOREBOARD))
        self.rect.x = 520
        self.rect.y = 405
