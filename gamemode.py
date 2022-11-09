import enum


class GameMode:
    START = enum.auto()
    PLAYING = enum.auto()
    DEAD = enum.auto()

    state = START
