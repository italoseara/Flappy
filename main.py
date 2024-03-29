import os

from constants import DEFAULT_WIN_SIZE, Graphics, Sounds
from gameengine import resources
from gameengine.engine import Program
from gameengine.window import Window
from mainscene import MainScene


def load_assets():
    graphics_data = {
        # general
        Graphics.ICON: "icon.bmp",
        # font - numbers
        Graphics.CHAR_B0: "numbers/big/0.png",
        Graphics.CHAR_B1: "numbers/big/1.png",
        Graphics.CHAR_B2: "numbers/big/2.png",
        Graphics.CHAR_B3: "numbers/big/3.png",
        Graphics.CHAR_B4: "numbers/big/4.png",
        Graphics.CHAR_B5: "numbers/big/5.png",
        Graphics.CHAR_B6: "numbers/big/6.png",
        Graphics.CHAR_B7: "numbers/big/7.png",
        Graphics.CHAR_B8: "numbers/big/8.png",
        Graphics.CHAR_B9: "numbers/big/9.png",
        Graphics.CHAR_S0: "numbers/small/0.png",
        Graphics.CHAR_S1: "numbers/small/1.png",
        Graphics.CHAR_S2: "numbers/small/2.png",
        Graphics.CHAR_S3: "numbers/small/3.png",
        Graphics.CHAR_S4: "numbers/small/4.png",
        Graphics.CHAR_S5: "numbers/small/5.png",
        Graphics.CHAR_S6: "numbers/small/6.png",
        Graphics.CHAR_S7: "numbers/small/7.png",
        Graphics.CHAR_S8: "numbers/small/8.png",
        Graphics.CHAR_S9: "numbers/small/9.png",
        # tiles
        Graphics.FLOOR: "tiles/floor.png",
        Graphics.BG_BUSH: "tiles/bush.png",
        Graphics.BG_CITY: "tiles/city.png",
        Graphics.BG_CLOUDS: "tiles/clouds.png",
        Graphics.PIPE_TOP: "tiles/pipe_top.png",
        Graphics.PIPE_BOT: "tiles/pipe_bot.png",
        # bird
        Graphics.PLAYER_F0: "bird/bird_f0.png",
        Graphics.PLAYER_F1: "bird/bird_f1.png",
        # text
        Graphics.MSG_GAME_OVER: "text/msg_game_over.png",
        Graphics.MSG_FLAPPY: "text/msg_flappy.png",
        Graphics.MSG_READY: "text/msg_ready.png",
        # ui.buttons
        Graphics.BTN_PAUSE_NORMAL: "ui/buttons/btn_pause_normal.png",
        Graphics.BTN_PAUSE_PAUSED: "ui/buttons/btn_pause_paused.png",
        Graphics.BTN_PLAY: "ui/buttons/btn_play.png",
        Graphics.BTN_SCOREBOARD: "ui/buttons/btn_scoreboard.png",
        # ui.boxes
        Graphics.BOX_MENU: "ui/boxes/box_menu.png",
        Graphics.BOX_END: "ui/boxes/box_end.png",
        # ui.etc
        Graphics.STARTER_TIP: "ui/etc/starter_tip.png",
        # ui.medals
        Graphics.MEDAL_BRONZE: "ui/medals/medal_bronze.png",
        Graphics.MEDAL_SILVER: "ui/medals/medal_silver.png",
        Graphics.MEDAL_GOLD: "ui/medals/medal_gold.png",
    }
    graphics_path = "assets/images/"

    for enum, path in graphics_data.items():
        resources.surface.add_from_file(enum, os.path.join(graphics_path, path))

    sounds_data = {
        Sounds.WING: "wing.wav",
        Sounds.HIT: "hit.wav",
        Sounds.POINT: "point.wav",
        Sounds.DIE: "die.wav",
    }
    sounds_path = "assets/audio/"

    for enum, path in sounds_data.items():
        resources.sound.add_from_file(enum, os.path.join(sounds_path, path))


class Flappy(Program):
    def __init__(self):
        super().__init__(Window(DEFAULT_WIN_SIZE), 60)

        self.window.set_title("Flappy Birds")
        load_assets()
        self.window.set_icon(resources.surface.get(Graphics.ICON))

        self.set_scene(MainScene())


if __name__ == "__main__":
    Flappy().start_loop()
