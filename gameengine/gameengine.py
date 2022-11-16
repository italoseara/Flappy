import pygame

from .display import Display
from .mouse import Mouse
from .window import Window

pygame.init()


class GameEngine:
    display = None
    scene = None
    request_quit = False
    framerate = None
    deltatime = 1
    clock = pygame.time.Clock()

    @classmethod
    def set_window_size(cls, size, *flags, update_display=True):
        Window.set_size(size, *flags)
        if update_display:
            Display.set_display_from_window()

    @classmethod
    def set_framerate(cls, framerate):
        cls.framerate = framerate

    @classmethod
    def update_events(cls):
        cls.request_quit = len(pygame.event.get(pygame.QUIT)) > 0

        Mouse.update(
            *pygame.event.get(pygame.MOUSEBUTTONDOWN),
            *pygame.event.get(pygame.MOUSEBUTTONUP),
            *pygame.event.get(pygame.MOUSEMOTION),
            *pygame.event.get(pygame.MOUSEWHEEL),
        )

    @classmethod
    def tick_clock(cls):
        cls.deltatime = cls.clock.tick(cls.framerate) / 1000

    @classmethod
    def set_scene(cls, scene):
        cls.scene = scene

    @classmethod
    def quit(cls):
        raise SystemExit(0)

    @classmethod
    def start_loop(cls):
        while True:
            cls.update_events()
            cls.scene.update()

            if Window._sdl2_window.size != Display.get_size():
                cls.scene.draw(Display.display_surface, Display.background)
                pygame.transform.scale(
                    Display.display_surface,
                    Window._sdl2_window.size,
                    Window.window_surface,
                )
            else:
                cls.scene.draw(Window.window_surface, Display.background)

            pygame.display.update()
            cls.tick_clock()
