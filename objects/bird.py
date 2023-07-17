from math import sin

import pygame

from constants import GameMode, Graphics, Sounds
from new_gameengine.animation import Animation
from new_gameengine.basechild import BaseChild
from new_gameengine import resources
from gamestate import GameState


class Bird(BaseChild):
    def __init__(self, program):
        super().__init__(
            program,
            Animation.from_assets(
                5,
                bird_f0 := resources.surface.get(Graphics.BIRD_F0),
                resources.surface.get(Graphics.BIRD_F1),
            ),
        )

        BIRD_CENTER_OFFSET_X = 50

        display = self.program.window.display
        self.rect.x = (
            display.width / 2 - bird_f0.get_height() / 2 - BIRD_CENTER_OFFSET_X
        )
        self.rect.y = display.height / 2 - bird_f0.get_height() / 2

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
            self.jump_counter += self.program.time.delta

            self.rect.y += self.speed.y * self.program.time.delta

            if GameState.game_mode == GameMode.START:
                self.speed.y = (
                    sin(self.__idle_frames * self.program.time.delta * 3) * 30
                )
                self.__idle_frames += 1
            else:
                self.speed.y += GameState.Config.gravity * self.program.time.delta

            if self.rect.y < 0:
                self.rect.y = 0
                self.speed.y = 0

            if GameState.game_mode == GameMode.DEAD:
                if self.hitbox.rect.bottom > GameState.Config.ground_line:
                    self.rect.y -= (
                        self.hitbox.rect.bottom - GameState.Config.ground_line
                    )
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
                    (self.angle_target - self.rotation.angle)
                    * 9.0
                    * self.program.time.delta
                )

            if (
                self.program.devices.mouse.get_pressed_in_frame(pygame.BUTTON_LEFT)
                or self.program.devices.keyboard.get_pressed_in_frame(
                    pygame.KEYDOWN, pygame.K_SPACE
                )
                or self.program.devices.keyboard.get_pressed_in_frame(
                    pygame.KEYDOWN, pygame.K_w
                )
                or self.program.devices.keyboard.get_pressed_in_frame(
                    pygame.KEYDOWN, pygame.K_UP
                )
            ):
                if GameState.game_mode == GameMode.START:
                    GameState.game_mode = GameMode.PLAYING

                if GameState.game_mode == GameMode.PLAYING:
                    self.jump()

    def die(self):
        GameState.game_mode = GameMode.DEAD
        pygame.mixer.Channel(2).play(resources.sound.get(Sounds.HIT))
        pygame.mixer.Channel(3).play(resources.sound.get(Sounds.DIE))

        self.animation.pause()

        self.jump()

    def jump(self):
        if GameState.game_mode == GameMode.PLAYING:
            pygame.mixer.Channel(0).play(resources.sound.get(Sounds.WING))

        self.speed.y = GameState.Config.jump_speed
        self.jump_counter = 0
