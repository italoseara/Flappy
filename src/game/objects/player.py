import pygame

from math import sin

from core.entity import SimpleEntity
from core.maths import Vector2
from core.data import PygameSurface
from game.data import GameMode

class Player(SimpleEntity):
    def __init__(self, pos, frames):
        super().__init__(pos, frames)

        self.fixed_hitbox = self.hitbox

        # reset-able variables
        self.speed = Vector2(0, 0)
        self.angle = 0
        self.angle_target = 0
        self.health = 0
        self.jump_counter = 0
        self.animation_id = 0
        self.animation_timer_limit = 0
        self.animation_timer = 0

    def reset(self):
        self.speed = Vector2(0, 0)
        self.angle = 0
        self.angle_target = 0
        self.health = 0
        self.jump_counter = 0
        self.animation_id = 0
        self.animation_timer_limit = 0
        self.animation_timer = 0

    def process(self):
        pass

    def process_extra(self, state):
        self.jump_counter += 1

        # MOVEMENT ###########################

        self.pos.y += self.speed.y

        if state.game_mode == GameMode.START:
            self.speed.y = 0
            self.pos.y += sin(state.turn_timer / 8)
        else:
            self.speed.y += state.config.gravity

        # cap the Y speed if the player goes through the top of the screen
        if self.pos.y < 0:
            self.pos.y = 0
            self.speed.y = 0

        # let the player stuck above the ground
        if state.game_mode == GameMode.DEAD:
            ground_line_offset = state.config.ground_line - self.frames.current_frame.size.y - 5
            if self.pos.y > ground_line_offset:
                self.pos.y = ground_line_offset
                self.speed.y = 0

        # die when touch the ground
        elif (self.pos.y >= state.config.ground_line - self.fixed_hitbox[3]
              and state.game_mode == GameMode.PLAYING):
            self.pos.y = state.config.ground_line - self.fixed_hitbox[3]
            state.game_mode = GameMode.DEAD
            self.speed.y = -8

        if self.animation_id == 0:
            # introduction (flying)
            self.animation_timer_limit = 6
        elif self.animation_id == 1:
            # transition to stop the wings (when dying)
            self.animation_timer_limit = 8
            if self.frames.current_index == 0:
                self.animation_id = 2
        elif self.animation_id == 2:
            # stopped wings
            self.animation_timer_limit = None

        if self.animation_id is not None:
            self.animation_timer += 1

        if self.animation_timer == self.animation_timer_limit:
            self.frames.current_index += 1
            if self.frames.current_index >= len(self.frames.frame_list):
                self.frames.current_index = 0
            self.animation_timer = 0

        # rotate the player based on when has it jumped.
        if state.game_mode != GameMode.START:
            if self.jump_counter < 30:
                self.angle_target = 30
            else:
                self.angle_target = -45

            self.angle += (self.angle_target - self.angle) * 0.15
            self.angle_target = (self.angle_target + 360) % 360

    def get_render(self):
        old_center = (self.pos.x + 15, self.pos.y + 15)

        new_image = pygame.transform.rotate(
            self.frames.current_frame.inner, self.angle
        )

        rect = new_image.get_rect()
        rect.center = old_center

        return (PygameSurface(new_image), (rect.x, rect.y))
