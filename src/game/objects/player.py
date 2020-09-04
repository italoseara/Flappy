import pygame

from math import sin

from core.entity import Entity
from core.data import Vector2D
from core.maths import gameobject_hitbox, gameobject_size

class Player(Entity):
    def __init__(self, pos, frames):
        self.setup(pos, frames)
        self.reset()

    def reset(self):
        self.speed = Vector2D(0, 0)
        self.angle = 0
        self.angle_target = 0
        self.health = 0
        self.fixed_hitbox = gameobject_hitbox(self)
        self.jump_counter = 0
        self.animation_id = 0
        self.animation_timer_limit = 0
        self.animation_timer = 0

    def process(self, state, config):
        ih = state.input_handler

        self.jump_counter += 1

        # when pressing the up key
        if ih.keymap[pygame.K_UP].first:
            # start the game if it hasn't started yet
            # TODO: move this to __init__.py
            if state.game_state == 0:
                state.game_state = 1

            # jump
            if state.game_state in {0, 1}:
                self.speed.y = -8
                self.jump_counter = 0

        # MOVIMENTO ###########################

        self.pos.y += self.speed.y
        if state.game_state == 0:
            self.speed.y = 0
            self.pos.y += sin(state.game_timer / 10)
        else:
            self.speed.y += config.gravity

        # cap the Y speed if the player goes through the top of the screen
        if self.pos.y < 0:
            self.pos.y = 0
            self.speed.y = 0

        # let the player stuck above the ground
        # FIXME: make this less trash
        if self.pos.y > ((config.ground_pos - gameobject_size(self)[1]) - 5) and state.game_state == 2:
            self.pos.y = ((config.ground_pos - gameobject_size(self)[1]) - 5)
            self.speed.y = 0

        elif (self.pos.y >= config.ground_pos - self.fixed_hitbox[3]
              and state.game_state == 1):
            self.pos.y = config.ground_pos - self.fixed_hitbox[3]
            state.game_state = 2
            self.speed.y = -8

        if self.animation_id == 0:
            # introduction (flying)
            self.animation_timer_limit = 8
        elif self.animation_id == 1:
            # transition to stop the wings (when dying)
            self.animation_timer_limit = 8
            if self.frames.current_index == 0:
                self.animation_id = 2
        elif self.animation_id == 2:
            # stopped wings
            self.animation_timer_limit = None

        if self.animation_id != None:
            self.animation_timer += 1

        if self.animation_timer == self.animation_timer_limit:
            self.frames.current_index += 1
            if self.frames.current_index >= len(self.frames.frame_list):
                self.frames.current_index = 0
            self.animation_timer = 0

        # rotate the player based on when has it jumped.
        if state.game_state != 0:
            if self.jump_counter < 30:
                self.angle_target = 30
            else:
                self.angle_target = -45

            self.angle += (self.angle_target - self.angle) * 0.15
            self.angle_target = (self.angle_target + 360) % 360

    def render(self):
        # update the image and return it
        old_center = (self.pos.x + 15, self.pos.y + 15)
        new_image = pygame.transform.rotate(
            self.frames.current_frame, self.angle
        )
        rect = new_image.get_rect()
        rect.center = old_center

        return (new_image, rect)
