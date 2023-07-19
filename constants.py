from enum import Enum, IntEnum, auto

import pygame

DEFAULT_WIN_SIZE = pygame.Vector2(960, 540)


class Graphics(IntEnum):
    ICON = auto()

    CHAR_B0 = auto()
    CHAR_B1 = auto()
    CHAR_B2 = auto()
    CHAR_B3 = auto()
    CHAR_B4 = auto()
    CHAR_B5 = auto()
    CHAR_B6 = auto()
    CHAR_B7 = auto()
    CHAR_B8 = auto()
    CHAR_B9 = auto()

    CHAR_S0 = auto()
    CHAR_S1 = auto()
    CHAR_S2 = auto()
    CHAR_S3 = auto()
    CHAR_S4 = auto()
    CHAR_S5 = auto()
    CHAR_S6 = auto()
    CHAR_S7 = auto()
    CHAR_S8 = auto()
    CHAR_S9 = auto()

    FLOOR = auto()
    BG_BUSH = auto()
    BG_CITY = auto()
    BG_CLOUDS = auto()
    PIPE_TOP = auto()
    PIPE_BOT = auto()

    BIRD_F0 = auto()
    BIRD_F1 = auto()

    MSG_GAME_OVER = auto()
    MSG_FLAPPY = auto()
    MSG_READY = auto()

    BTN_PAUSE_NORMAL = auto()
    BTN_PAUSE_PAUSED = auto()
    BTN_PLAY = auto()
    BTN_SCOREBOARD = auto()

    BOX_MENU = auto()
    BOX_END = auto()

    MEDAL_BRONZE = auto()
    MEDAL_SILVER = auto()
    MEDAL_GOLD = auto()

    STARTER_TIP = auto()


class Sounds(IntEnum):
    WING = auto()
    HIT = auto()
    POINT = auto()
    DIE = auto()


class GameMode(Enum):
    START = 0
    PLAYING = 1
    DEAD = 2
