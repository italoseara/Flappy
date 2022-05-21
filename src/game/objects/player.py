import pygame

from math import sin
from typing import Tuple

from game.data import GameMode
from core.entity import SimpleEntity
from core.maths import Vector2
from core.data import PygameSurface

from game.data import Aud

class Player(SimpleEntity):
    def __init__(self, pos, frames):
        super().__init__(pos, frames)

        self.size = Vector2(self.hitbox.width, self.hitbox.height)
        self.fixed_hitbox = self.hitbox

        # reset-able variables
        self.speed = Vector2(0, 0)
        self.angle = 0
        self.angle_target = 0
        self.health = 0
        self.jump_counter = 0
        self.animation_id = 0
        self.animation_time_next_frame = 0 # FIXME: name is ambiguous - "time for next frame" actually means the remaining time for the next animation frame
        self.animation_timer = 0

    def reset(self):
        self.speed = Vector2(0, 0)
        self.angle = 0
        self.angle_target = 0
        self.health = 0
        self.jump_counter = 0
        self.animation_id = 0
        self.animation_time_next_frame = 0
        self.animation_timer = 0

    def process(self, state):
        pass

    def process_extra(self, state):
        self.jump_counter += state.delta_time

        # MOVEMENT ###########################

        self.pos.y += self.speed.y * state.delta_time

        if state.game_mode == GameMode.START:
            self.speed.y = sin(state.turn_timer * state.delta_time * 3) * 30
        else:
            self.speed.y += state.config.gravity * state.delta_time

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
        elif (
            self.pos.y >= state.config.ground_line - self.fixed_hitbox[3]
            and state.game_mode == GameMode.PLAYING
        ):
            self.pos.y = state.config.ground_line - self.fixed_hitbox[3]
            self.die(state=state)

        if self.animation_id is not None:
            self.animation_timer += state.delta_time
        else:
            self.animation_id = 0.0

        self.process_time_for_next_frame()
        while self.animation_timer >= self.animation_time_next_frame:
            self.frames.current_index = (self.frames.current_index + 1) % len(self.frames.frame_list)
            self.animation_timer -= self.animation_time_next_frame
            self.process_time_for_next_frame()

        # rotate the player based on when has it jumped.
        if state.game_mode != GameMode.START:
            self.angle_target = 30 if (self.jump_counter < 0.5) else -45

            self.angle += (self.angle_target - self.angle) * 9.0 * state.delta_time
            self.angle_target = (self.angle_target + 360) % 360

    def process_time_for_next_frame(self):
        NORMAL_FLIGHT_TIME = 0.2

        if self.animation_id == 0:
            # introduction (flying)
            self.animation_time_next_frame = NORMAL_FLIGHT_TIME
        elif self.animation_id == 1:
            # transition to stop the wings (when dying)
            self.animation_time_next_frame = NORMAL_FLIGHT_TIME
            if self.frames.current_index == 0:
                self.animation_id = 2
        elif self.animation_id == 2:
            # stopped wings
            self.animation_time_next_frame = None

    def die(self, state):
        state.game_mode = GameMode.DEAD
        self.jump(state=state)

    def jump(self, state, sound_fx=None):
        if sound_fx is not None:
            pygame.mixer.Channel(0).play(sound_fx)

        self.speed.y = state.config.jump_speed
        self.jump_counter = 0

    def get_render(self) -> Tuple[PygameSurface, Vector2]:
        old_center = (int(self.pos.x) + 15, int(self.pos.y) + 15)

        new_image = pygame.transform.rotate(
            self.frames.current_frame.inner, self.angle
        )

        rect = new_image.get_rect()
        rect.center = old_center

        return (PygameSurface(new_image), Vector2(rect.x, rect.y))
