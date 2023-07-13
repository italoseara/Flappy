from math import sin

import pygame

from constants import GameMode, Graphics, Sounds
from gameengine.animation import Animation
from gameengine.basechild import BaseChild
from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.resources import Resources
from gamestate import GameState


class Bird(BaseChild):
    def __init__(self):
        super().__init__(
            Animation.from_assets(
                5,
                Resources.Surface.get(Graphics.BIRD_F0),
                Resources.Surface.get(Graphics.BIRD_F1),
            )
        )

        self.offset.xy = self.rect.center

        self.rect.x = (
            Display.width / 2
            - Resources.Surface.get(Graphics.BIRD_F0).get_height() / 2
            - self.offset.x
        )
        self.rect.y = (
            Display.height / 2
            - Resources.Surface.get(Graphics.BIRD_F0).get_height() / 2
        )

        self.reset()

    def reset(self):
        self.__idle_frames = 0
        self.speed = pygame.Vector2(0, 0)
        self.angle_target = 0
        self.health = 0
        self.jump_counter = 0

    def update(self):
        super().update()

        if not GameState.is_paused:
            self.jump_counter += Engine.deltatime

            self.rect.y += self.speed.y * Engine.deltatime

            if GameState.game_mode == GameMode.START:
                self.speed.y = sin(self.__idle_frames * Engine.deltatime * 3) * 30
                self.__idle_frames += 1
            else:
                self.speed.y += GameState.Config.gravity * Engine.deltatime

            if self.rect.y < 0:
                self.rect.y = 0
                self.speed.y = 0

            if GameState.game_mode == GameMode.DEAD:
                ground_line_offset = GameState.Config.ground_line - self.rect.height - 5
                if self.rect.y > ground_line_offset:
                    self.rect.y = ground_line_offset
                    self.speed.y = 0

            elif (
                self.rect.y >= GameState.Config.ground_line - self.rect.height
                and GameState.game_mode == GameMode.PLAYING
            ):
                self.rect.y = GameState.Config.ground_line - self.rect.height
                self.die()

            if GameState.game_mode != GameMode.START:
                self.angle_target = 30 if self.jump_counter < 0.5 else -45
                self.rotation.angle += (
                    (self.angle_target - self.rotation.angle) * 9.0 * Engine.deltatime
                )

    def die(self):
        GameState.game_mode = GameMode.DEAD
        self.jump()

    def jump(self):
        if GameState.game_mode == GameMode.PLAYING:
            pygame.mixer.Channel(0).play(Resources.Sound.get(Sounds.WING))

        self.speed.y = GameState.Config.jump_speed
        self.jump_counter = 0
