import math

import pygame
import pygame._sdl2

from gameengine.mouse import Mouse

pygame.init()


class GameEngine:
    scaled_display = None
    scaled_display_rect = pygame.Rect(0, 0, 0, 0)
    display = None
    display_rect = None
    window = None
    clock = None
    current_scene = None
    background = None
    _scale = pygame.Vector2(1, 1)
    events = ()
    framerate = 60
    deltatime = 1 / framerate

    @classmethod
    def init(cls):
        cls.clock = pygame.time.Clock()

    @classmethod
    def get_mouse_pos(cls):
        pos = pygame.mouse.get_pos()
        return (pos[0] / cls._scale.x, pos[1] / cls._scale.y)

    @classmethod
    def get_display_size(cls):
        return cls.scaled_display_rect.size

    @classmethod
    def get_window_size(cls):
        return cls.display_rect.size

    @classmethod
    def get_scale(self):
        return self._scale.xy

    @classmethod
    def set_window_size(cls, size, *flags):
        flag = 0
        for f in flags:
            flag |= f
        cls.display = pygame.display.set_mode(size, flag)
        cls.window = pygame._sdl2.Window.from_display_module()
        cls.display_rect = cls.display.get_rect()
        cls._update_scale(size)

        cls.background = cls.display.convert()

    @classmethod
    def set_window_title(cls, title):
        pygame.display.set_caption(title)

    @classmethod
    def _update_scale(cls, size):
        x, y = cls._scale.xy
        size = (math.ceil(size[0] / x), math.ceil(size[1] / y))
        cls.scaled_display = pygame.Surface(size)
        cls.scaled_display_rect.size = cls.scaled_display.get_size()

    @classmethod
    def set_scale(cls, *scale):
        cls._scale = pygame.Vector2(*scale)
        cls._update_scale(cls.window.size)

    @classmethod
    def update_events(cls):
        cls.events = pygame.event.get()
        Mouse.update(cls)

    @classmethod
    def update_clock(cls):
        cls.deltatime = cls.clock.tick(cls.framerate) / 1000

    @classmethod
    def set_current_scene(cls, scene):
        cls.current_scene = scene

    @classmethod
    def request_exit(cls):
        raise SystemExit(0)

    @classmethod
    def start_loop(cls):
        cls.init()
        while True:
            cls.update_events()
            cls.current_scene.update()

            if cls.window.size != cls.scaled_display.get_size():
                cls.current_scene.draw(cls.scaled_display, cls.background)
                pygame.transform.scale(cls.scaled_display, cls.window.size, cls.display)
            else:
                cls.current_scene.draw(cls.display, cls.background)

            pygame.display.update()
            cls.update_clock()
