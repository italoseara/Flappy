import math
import os

import pygame

from constants import DEFAULT_WIN_SIZE, SKY_COLOR
from gameengine import Animations, Display, GameEngine, GameResources, Mouse, Window
from gamemode import GameMode
from scenary import ScenaryGroup


class Bird(pygame.sprite.DirtySprite):
    def __init__(self):
        super().__init__()

        self.pos = pygame.Vector2(0, 0)

        self.animation = Animations.get_animation("bird_fly", 5)

        self.origin_image = self.animation.get_current_frame()
        self.image = self.origin_image
        self.rect = self.image.get_rect()
        self.dirty = 2

        self.speed_y = 0
        self.accel = 0
        self.angle = 0

        self.dt_count = 0

        self.gravity = 1000
        self.speed = -400

    def prepare(self):
        self.speed_y = 0
        self.accel = 0

        OFFSET_X = 50
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

        self.accel += 1
        self.speed_y += self.accel * GameEngine.deltatime
        self.dt_count += GameEngine.deltatime

        if GameMode.state == GameMode.START:
            self.speed_y = math.sin(self.accel * GameEngine.deltatime * 3) * 30
        elif GameMode.state == GameMode.PLAYING:
            self.speed_y += self.gravity * GameEngine.deltatime
            if Mouse.get_pressed_event(pygame.BUTTON_LEFT):
                self.jump()

        # Angle select
        if GameMode.state != GameMode.START:
            angle_target = 30 if self.dt_count < 0.5 else -45

            self.angle += (angle_target - self.angle) * 9 * GameEngine.deltatime

        self.animation.update(GameEngine.deltatime)
        self.origin_image = self.animation.get_current_frame()

        self.image = pygame.transform.rotate(self.origin_image, self.angle)
        self.rect.size = self.image.get_size()

        self.pos.y += self.speed_y * GameEngine.deltatime
        self.rect.topleft = self.pos.xy
        # Temp
        self.rect.y %= Display.get_size()[1]


class MainScene(pygame.sprite.LayeredDirty):
    def __init__(self):
        super().__init__()
        self.bird = Bird()

        self.bird.prepare()

        self.add(self.bird, ScenaryGroup())

        self.change_layer(self.bird, self.bird._layer + 1)

    def update(self):
        super().update()
        if Mouse.get_pressed_event(pygame.BUTTON_LEFT):
            if GameMode.state == GameMode.START:
                GameMode.state = GameMode.PLAYING
                self.bird.jump()

        if GameEngine.request_quit:
            GameEngine.quit()


class Game:
    def __init__(self):
        Window.set_title("Flappy Bird [Python]")

        GameEngine.set_window_size(DEFAULT_WIN_SIZE)
        GameEngine.set_framerate(60)

        Display.background = Window.window_surface.convert()
        Display.background.fill(SKY_COLOR)
        self.load_resources()

        GameEngine.set_scene(GameResources.Scenes.get_scene("main"))

    def run(self):
        GameEngine.start_loop()

    def load_resources(self):
        paths = {
            # general
            "ICON": "icon.bmp",
            # font - numbers
            "CHAR_B0": "numbers/big/0.png",
            "CHAR_B1": "numbers/big/1.png",
            "CHAR_B2": "numbers/big/2.png",
            "CHAR_B3": "numbers/big/3.png",
            "CHAR_B4": "numbers/big/4.png",
            "CHAR_B5": "numbers/big/5.png",
            "CHAR_B6": "numbers/big/6.png",
            "CHAR_B7": "numbers/big/7.png",
            "CHAR_B8": "numbers/big/8.png",
            "CHAR_B9": "numbers/big/9.png",
            "CHAR_S0": "numbers/small/0.png",
            "CHAR_S1": "numbers/small/1.png",
            "CHAR_S2": "numbers/small/2.png",
            "CHAR_S3": "numbers/small/3.png",
            "CHAR_S4": "numbers/small/4.png",
            "CHAR_S5": "numbers/small/5.png",
            "CHAR_S6": "numbers/small/6.png",
            "CHAR_S7": "numbers/small/7.png",
            "CHAR_S8": "numbers/small/8.png",
            "CHAR_S9": "numbers/small/9.png",
            # tiles
            "FLOOR": "tiles/floor.png",
            "BG_BUSH": "tiles/bush.png",
            "BG_CITY": "tiles/city.png",
            "BG_CLOUDS": "tiles/clouds.png",
            "PIPE_TOP": "tiles/pipe_top.png",
            "PIPE_BOT": "tiles/pipe_bot.png",
            # bird
            "BIRD_F0": "bird/bird_f0.png",
            "BIRD_F1": "bird/bird_f1.png",
            # text
            "MSG_GAME_OVER": "text/msg_game_over.png",
            "MSG_FLAPPY": "text/msg_flappy.png",
            "MSG_READY": "text/msg_ready.png",
            # ui.buttons
            "BTN_PAUSE_NORMAL": "ui/buttons/btn_pause_normal.png",
            "BTN_PAUSE_PAUSED": "ui/buttons/btn_pause_paused.png",
            "BTN_PLAY": "ui/buttons/btn_play.png",
            "BTN_SCOREBOARD": "ui/buttons/btn_scoreboard.png",
            # ui.boxes
            "BOX_MENU": "ui/boxes/box_menu.png",
            "BOX_END": "ui/boxes/box_end.png",
            # ui.etc
            "STARTER_TIP": "ui/etc/starter_tip.png",
            # ui.medals
            "MEDAL_BRONZE": "ui/medals/medal_bronze.png",
            "MEDAL_SILVER": "ui/medals/medal_silver.png",
            "MEDAL_GOLD": "ui/medals/medal_gold.png",
        }

        for name, relpath in paths.items():
            GameResources.Surface.add_surface_from_file(
                name, os.path.join("resources/", relpath)
            )
        GameResources.Scenes.add_scene("main", MainScene)

        Animations.add_animation_data(
            "bird_fly",
            Animations.FRAME_TYPE,
            GameResources.Surface.get_surface("BIRD_F0"),
        )
        Animations.add_animation_data(
            "bird_fly",
            Animations.FRAME_TYPE,
            GameResources.Surface.get_surface("BIRD_F1"),
        )


if __name__ == "__main__":
    Game().run()
