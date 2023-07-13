import pygame

from constants import GameMode
from gameengine.basescene import BaseScene
from gameengine.engine import Engine
from gameengine.mouse import Mouse
from gamestate import GameState
from objects.bird import Bird
from objects.city import City
from objects.clouds import Clouds


class MainScene(BaseScene):
    def __init__(self):
        super().__init__()

        self.bg = (11, 200, 215)

        self.bird = Bird()

        self.add_children(Clouds(), City(), self.bird)

    def update(self):
        if Engine.request_quit:
            Engine.system_exit()

        if Mouse.get_pressed_in_frame(pygame.BUTTON_LEFT):
            if GameState.game_mode == GameMode.START:
                GameState.game_mode = GameMode.PLAYING

            if GameState.game_mode == GameMode.PLAYING:
                self.bird.jump()

        # pipes process

        super().update()
