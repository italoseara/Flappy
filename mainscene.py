import pygame

from constants import GameMode
from gameengine.basescene import BaseScene
from gameengine.engine import Engine
from gameengine.keyboard import Keyboard
from gameengine.mouse import Mouse
from gamestate import GameState
from objects.bird import Bird
from objects.bush import Bush
from objects.city import City
from objects.clouds import Clouds
from objects.floor import Floor
from objects.pausebutton import PauseButton


class MainScene(BaseScene):
    def __init__(self):
        super().__init__()

        self.bg = (11, 200, 215)

        self.pause_button = PauseButton()
        self.bird = Bird()

        self.add_children(
            Clouds(), City(), Bush(), Floor(), self.bird, self.pause_button
        )

    def update(self):
        if Engine.request_quit:
            Engine.system_exit()

        if Mouse.get_pressed_in_frame(pygame.BUTTON_LEFT):
            if GameState.game_mode == GameMode.START:
                GameState.game_mode = GameMode.PLAYING

            if GameState.game_mode == GameMode.PLAYING:
                self.bird.jump()

        should_pause = (
            Keyboard.get_pressed(pygame.K_ESCAPE)
            and GameState.game_mode != GameMode.DEAD
            or ()
        )

        super().update()
