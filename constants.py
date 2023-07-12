import enum
from dataclasses import dataclass


class Graphics(enum.IntEnum):
    ICON = enum.auto()

    CHAR_B0 = enum.auto()
    CHAR_B1 = enum.auto()
    CHAR_B2 = enum.auto()
    CHAR_B3 = enum.auto()
    CHAR_B4 = enum.auto()
    CHAR_B5 = enum.auto()
    CHAR_B6 = enum.auto()
    CHAR_B7 = enum.auto()
    CHAR_B8 = enum.auto()
    CHAR_B9 = enum.auto()

    CHAR_S0 = enum.auto()
    CHAR_S1 = enum.auto()
    CHAR_S2 = enum.auto()
    CHAR_S3 = enum.auto()
    CHAR_S4 = enum.auto()
    CHAR_S5 = enum.auto()
    CHAR_S6 = enum.auto()
    CHAR_S7 = enum.auto()
    CHAR_S8 = enum.auto()
    CHAR_S9 = enum.auto()

    FLOOR = enum.auto()
    BG_BUSH = enum.auto()
    BG_CITY = enum.auto()
    BG_CLOUDS = enum.auto()
    PIPE_TOP = enum.auto()
    PIPE_BOT = enum.auto()

    BIRD_F0 = enum.auto()
    BIRD_F1 = enum.auto()

    MSG_GAME_OVER = enum.auto()
    MSG_FLAPPY = enum.auto()
    MSG_READY = enum.auto()

    BTN_PAUSE_NORMAL = enum.auto()
    BTN_PAUSE_PAUSED = enum.auto()
    BTN_PLAY = enum.auto()
    BTN_SCOREBOARD = enum.auto()

    BOX_MENU = enum.auto()
    BOX_END = enum.auto()

    MEDAL_BRONZE = enum.auto()
    MEDAL_SILVER = enum.auto()
    MEDAL_GOLD = enum.auto()

    STARTER_TIP = enum.auto()


print(Graphics.ICON)
