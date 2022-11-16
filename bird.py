import math

import pygame

from constants import OFFSET_X
from gameengine import Animations, Display, GameEngine, Mouse
from gamemode import GameMode


class Bird(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()

        self.pos = pygame.Vector2(0, 0)

        self.animation = Animations.get_animation("bird_fly", 5)

        self.origin_image = self.animation.get_current_frame()
        self.image = self.origin_image
        self.rect = self.image.get_rect()

        self.speed_y = 0
        self.accel = 0
        self.angle = 0

        self.dt_count = 0

        self.gravity = 1000
        self.speed = -400

        self.dirty = 2

    def prepare(self):
        self.speed_y = 0
        self.accel = 0

        rect = pygame.Rect((0, 0), self.rect.size)
        display_rect = Display.display_surface.get_rect()
        rect.center = display_rect.center
        self.pos.xy = rect.topleft
        self.pos.x -= OFFSET_X

    def jump(self):
        self.speed_y = self.speed
        self.accel = 0
        self.dt_count = 0

    def update(self):
        super().update()

        # update velocity vars
        self.accel += 1
        self.speed_y += self.accel * GameEngine.deltatime
        self.dt_count += GameEngine.deltatime

        # apply speed y
        if GameMode.state == GameMode.START:
            self.speed_y = math.sin(self.accel * GameEngine.deltatime * 3) * 30
        elif GameMode.state == GameMode.PLAYING:
            self.speed_y += self.gravity * GameEngine.deltatime

        # angle select
        if GameMode.state != GameMode.START:
            angle_target = 30 if self.dt_count < 0.5 else -45

            self.angle += (angle_target - self.angle) * 9 * GameEngine.deltatime

        # update animation
        self.animation.update(GameEngine.deltatime)
        self.origin_image = self.animation.get_current_frame()

        # rotate image
        self.image = pygame.transform.rotate(self.origin_image, self.angle)
        self.rect.size = self.image.get_size()

        # apply pos in rect
        self.pos.y += self.speed_y * GameEngine.deltatime
        self.rect.topleft = self.pos.xy

        # Temp
        self.rect.y %= Display.get_size()[1]

        if Mouse.get_pressed_event(pygame.BUTTON_LEFT):
            if GameMode.state == GameMode.START:
                GameMode.state = GameMode.PLAYING
            self.jump()
