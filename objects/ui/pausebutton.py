import pygame

from constants import GameMode, Graphics
from gameengine.animation import Animation
from gameengine.basechild import BaseChild
from gameengine.display import Display
from gameengine.keyboard import Keyboard
from gameengine.mouse import Mouse
from gameengine.resources import Resources
from gamestate import GameState


class PauseButton(BaseChild):
    def __init__(self):
        super().__init__(
            Animation.from_assets(
                1,
                Resources.Surface.get(Graphics.BTN_PAUSE_NORMAL),
                Resources.Surface.get(Graphics.BTN_PAUSE_PAUSED),
            )
        )
        self.image.pause()

        self.rect.right = Display.width - 10
        self.rect.y = 10

        self.pressed = False

    def update(self):
        self.active = GameState.game_mode == GameMode.PLAYING

        if self.active:
            self.pressed = self.rect.collidepoint(Mouse.pos) and Mouse.get_pressed_in_frame(
                pygame.BUTTON_LEFT
            )

            if (
                Keyboard.get_pressed_in_frame(pygame.KEYDOWN, pygame.K_ESCAPE)
                or self.pressed
            ) and GameState.game_mode != GameMode.DEAD:
                GameState.is_paused = not GameState.is_paused

            if GameState.is_paused:
                self.image.frame_index = 1
            else:
                self.image.frame_index = 0

            super().update()
