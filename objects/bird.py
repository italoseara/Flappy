from math import sin

import pygame

from constants import Graphics
from gameengine.animation import Animation
from gameengine.basechild import BaseChild
from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.resources import Resources


class Bird(BaseChild):
    BIRD_CENTER_OFFSET_X = 50

    def __init__(self):
        super().__init__(
            Animation.from_assets(
                5,
                Resources.Surface.get(Graphics.BIRD_F0),
                Resources.Surface.get(Graphics.BIRD_F1),
            )
        )
        self.rect.x = (
            Display.width / 2
            - Resources.Surface.get(Graphics.BIRD_F0).get_height() / 2
            - self.BIRD_CENTER_OFFSET_X
        )
        self.rect.y = (
            Display.height / 2
            - Resources.Surface.get(Graphics.BIRD_F0).get_height() / 2
        )

        self.reset()

    def reset(self):
        self.__idle_frames = 0
        self.speed = pygame.Vector2(0, 0)
        self.angle = 0
        self.angle_target = 0
        self.health = 0
        self.jump_counter = 0

    def update(self):
        super().update()

        if not self.parent.is_paused:
            self.jump_counter += Engine.deltatime

            self.rect.y += self.speed.y * Engine.deltatime
            self.speed.y = sin(self.__idle_frames * Engine.deltatime * 3) * 30
            self.__idle_frames += 1
