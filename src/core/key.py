import pygame

from enum import IntEnum, unique, auto
from dataclasses import dataclass
from typing import Set

from .maths import Vector2

@unique
class InputValue(IntEnum):
    ARROW_UP = auto()
    # ARROW_DOWN = auto()
    # ARROW_LEFT = auto()
    # ARROW_RIGHT = auto()

    W = auto()
    H = auto()

    MOUSE_BTN_LEFT = auto()
    MOUSE_BTN_MIDDLE = auto()
    MOUSE_BTN_RIGHT = auto()

    SPACE = auto()
    ESC = auto()

@dataclass
class KeyData:
    held: bool
    first: bool

class KeyHandler:
    PYGAME_REGISTER_MAP = {
        pygame.K_UP: InputValue.ARROW_UP,
        pygame.K_h: InputValue.H,
        pygame.K_w: InputValue.W,
        pygame.K_SPACE: InputValue.SPACE,
        pygame.K_ESCAPE: InputValue.ESC,
    }

    PYGAME_REGISTER_MAP_REV = {v: k for k, v in PYGAME_REGISTER_MAP.items()}

    UPKEYS_CHECK_SET = {
        InputValue.ARROW_UP,
        InputValue.W,
        InputValue.SPACE,
        InputValue.MOUSE_BTN_LEFT,
    }

    MOUSE_BTN_INDEXED = {
        0: InputValue.MOUSE_BTN_LEFT,
        1: InputValue.MOUSE_BTN_MIDDLE,
        2: InputValue.MOUSE_BTN_RIGHT,
    }

    def __init__(self):
        self._key_map = {}
        self._reserved_keys = set()
        self._upkeys = KeyData(False, False)

        self._mouse_pos = None

    def reserve_keys(self, keys: Set[InputValue]):
        for key in keys:
            self._reserved_keys.add(key)

    def is_first(self, code: InputValue) -> bool:
        """Gets the "first" value of the key identified by the code `code`.
        This "first" value/attribute means that, of a sequence of
        frames where the key is pressed, this is the first frame. This
        can be used in e.g. code for the player to jump.

        Throws a ValueError if the key is not reserved."""

        if code in self._reserved_keys:
            return self._key_map.get(code).first or False
        else:
            raise ValueError(f"code {code} is not reserved")

    def is_held(self, code: InputValue) -> bool:
        """Gets the "held" value of the key identified by the code `code`.

        Works pretty much the same as self.is_first, but for every
        frame the key has been pressed."""

        if code in self._reserved_keys:
            return self._key_map.get(code).first or False
        else:
            raise ValueError(f"code {code} is not reserved")

    def upkeys_first(self) -> bool:
        return self._upkeys.first

    def upkeys_held(self) -> bool:
        return self._upkeys.held

    @property
    def mouse_pos(self) -> Vector2:
        if self._mouse_pos is None:
            raise ValueError("mouse position has not been grabbed yet")
        else:
            return self._mouse_pos

    def update_keys(self):
        from_keyboard = pygame.key.get_pressed()
        from_mouse = pygame.mouse.get_pressed()

        for iv in self._reserved_keys:
            if iv not in KeyHandler.MOUSE_BTN_INDEXED.values():
                # get the key data
                data = self._key_map.get(iv) or KeyData(False, False)
                data.first = False

                # if the key has been pressed in the current frame
                if from_keyboard[KeyHandler.PYGAME_REGISTER_MAP_REV[iv]]:
                    # check if should mark as FIRST
                    if not data.held:
                        data.first = True

                    # always mark as HELD
                    data.held = True
                else:
                    data.held = False

                # place back the key data
                self._key_map[iv] = data

        # mouse
        for i, v in KeyHandler.MOUSE_BTN_INDEXED.items():
            if v in self._reserved_keys:
                data = self._key_map.get(v) or KeyData(False, False)
                data.first = False

                if from_mouse[i]:
                    if not data.held:
                        data.first = True
                    data.held = True
                else:
                    data.held = False

                self._key_map[v] = data

        self._mouse_pos = Vector2.from_tuple(pygame.mouse.get_pos())

        self._upkeys.held = False
        self._upkeys.first = False

        for iv in KeyHandler.UPKEYS_CHECK_SET:
            if iv in self._reserved_keys and self._key_map[iv].first:
                self._upkeys.first = True
                break

        for iv in KeyHandler.UPKEYS_CHECK_SET:
            if iv in self._reserved_keys and self._key_map[iv].held:
                self._upkeys.held = True
                break
