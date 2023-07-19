import pygame

import state
from constants import GameMode, Graphics
from gameengine import resources
from gameengine.animation import Animation
from gameengine.basechild import BaseChild


class PauseButton(BaseChild):
    def __init__(self):
        super().__init__(
            Animation.from_assets(
                1,
                resources.surface.get(Graphics.BTN_PAUSE_NORMAL),
                resources.surface.get(Graphics.BTN_PAUSE_PAUSED),
            ),
        )
        self.animation.pause()

        self.rect.right = self.program.window.display.width - 10
        self.rect.y = 10

        self.pressed = False

    def update(self):
        self.active = state.game_mode == GameMode.PLAYING

        if self.active:
            self.pressed = (
                self.rect.collidepoint(self.program.devices.mouse.pos)
                and self.program.devices.mouse.get_pressed_in_frame(pygame.BUTTON_LEFT)
            ) or self.program.devices.keyboard.get_pressed_in_frame(
                pygame.KEYDOWN, pygame.K_ESCAPE
            )

            if self.pressed and state.game_mode != GameMode.DEAD:
                state.is_paused = not state.is_paused

            if state.is_paused:
                self.animation.frame_index = 1
            else:
                self.animation.frame_index = 0

            super().update()
