import pygame

from constants import GameMode, Graphics
from new_gameengine.animation import Animation
from new_gameengine.basechild import BaseChild
from new_gameengine import resources
from gamestate import GameState


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
        self.active = GameState.game_mode == GameMode.PLAYING

        if self.active:
            self.pressed = (
                self.rect.collidepoint(self.program.devices.mouse.pos)
                and self.program.devices.mouse.get_pressed_in_frame(pygame.BUTTON_LEFT)
            ) or self.program.devices.keyboard.get_pressed_in_frame(
                pygame.KEYDOWN, pygame.K_ESCAPE
            )

            if self.pressed and GameState.game_mode != GameMode.DEAD:
                GameState.is_paused = not GameState.is_paused

            if GameState.is_paused:
                self.animation.frame_index = 1
            else:
                self.animation.frame_index = 0

            super().update()
