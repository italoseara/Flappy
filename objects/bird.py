from math import sin

import pygame

from constants import GameMode, Graphics, Sounds
from gameengine.animation import Animation
from gameengine.basechild import BaseChild
from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.keyboard import Keyboard
from gameengine.mouse import Mouse
from gameengine.resources import Resources
from gamestate import GameState


class Bird(BaseChild):
    def __init__(self):
        super().__init__(
            Animation.from_assets(
                5,
                bird_f0 := Resources.Surface.get(Graphics.BIRD_F0),
                Resources.Surface.get(Graphics.BIRD_F1),
            )
        )

        BIRD_CENTER_OFFSET_X = 50
        self.rect.x = (
            Display.width / 2 - bird_f0.get_height() / 2 - BIRD_CENTER_OFFSET_X
        )
        self.rect.y = Display.height / 2 - bird_f0.get_height() / 2

        self.reset()

    def reset(self):
        self.__idle_frames = 0
        self.speed = pygame.Vector2(0, 0)
        self.angle_target = 0
        self.health = 0
        self.jump_counter = 0

    def update(self):
        if not GameState.is_paused:
            super().update()
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
                if self.hitbox.rect.bottom > GameState.Config.ground_line:
                    self.rect.y -= self.hitbox.rect.bottom - GameState.Config.ground_line
                    self.speed.y = 0

            elif (
                self.hitbox.rect.bottom >= GameState.Config.ground_line
                and GameState.game_mode == GameMode.PLAYING
            ):
                self.rect.y = GameState.Config.ground_line - self.hitbox.rect.h
                self.die()

            if GameState.game_mode != GameMode.START:
                self.angle_target = 30 if self.jump_counter < 0.5 else -45
                self.rotation.angle += (
                    (self.angle_target - self.rotation.angle) * 9.0 * Engine.deltatime
                )

            if (
                Mouse.get_pressed_in_frame(pygame.BUTTON_LEFT)
                or Keyboard.get_pressed_in_frame(pygame.KEYDOWN, pygame.K_SPACE)
                or Keyboard.get_pressed_in_frame(pygame.KEYDOWN, pygame.K_w)
                or Keyboard.get_pressed_in_frame(pygame.KEYDOWN, pygame.K_UP)
            ):
                if GameState.game_mode == GameMode.START:
                    GameState.game_mode = GameMode.PLAYING

                if GameState.game_mode == GameMode.PLAYING:
                    self.jump()

    def die(self):
        GameState.game_mode = GameMode.DEAD
        pygame.mixer.Channel(2).play(Resources.Sound.get(Sounds.HIT))
        pygame.mixer.Channel(3).play(Resources.Sound.get(Sounds.DIE))

        self.image.pause()

        self.jump()

    def jump(self):
        if GameState.game_mode == GameMode.PLAYING:
            pygame.mixer.Channel(0).play(Resources.Sound.get(Sounds.WING))

        self.speed.y = GameState.Config.jump_speed
        self.jump_counter = 0
