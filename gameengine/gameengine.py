import math

import pygame
import pygame._sdl2

from gameengine.mouse import Mouse

pygame.init()


class GameEngine:
    display = None
    screen_display = None
    _window = None
    clock = None
    current_scene = None
    background = None
    ref_scale = pygame.Vector2(1, 1)
    events = ()
    framerate = None
    deltatime = 1

    @classmethod
    def init(cls):
        cls.clock = pygame.time.Clock()

    @classmethod
    def set_framerate(cls, framerate):
        cls.framerate = framerate

    @classmethod
    def set_display_size(cls, size):
        cls.display = pygame.Surface(size, cls.display.get_flags())
        cls.ref_scale.xy = (
            cls.screen_display.get_width() / size[0],
            cls.screen_display.get_height() / size[1],
        )

    @classmethod
    def get_display_size(cls):
        return cls.display.get_size()

    @classmethod
    def get_window_size(cls):
        return pygame.display.get_window_size()

    @classmethod
    def set_window_size(cls, size, *flags):
        flag = 0
        for f in flags:
            flag |= f
        cls.screen_display = pygame.display.set_mode(size, flag)
        cls._window = pygame._sdl2.Window.from_display_module()

        cls.set_scale(cls.ref_scale.xy)

        cls.background = cls.screen_display.convert()

    @classmethod
    def get_scale(self):
        return self.ref_scale.xy

    @classmethod
    def set_scale(cls, *scale):
        cls.ref_scale = pygame.Vector2(*scale)
        if not cls.screen_display is None:
            cls.display = pygame.Surface(
                (
                    math.ceil(cls.screen_display.get_width() / cls.ref_scale.x),
                    (math.ceil(cls.screen_display.get_height() / cls.ref_scale.y)),
                )
            )

    @classmethod
    def set_window_title(cls, title):
        pygame.display.set_caption(title)

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

            if cls._window.size != cls.display.get_size():
                cls.current_scene.draw(cls.display, cls.background)
                pygame.transform.scale(
                    cls.display, cls._window.size, cls.screen_display
                )
            else:
                cls.current_scene.draw(cls.screen_display, cls.background)

            pygame.display.update()
            cls.update_clock()
