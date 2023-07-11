import pygame

from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.window import Window
from mainscene import MainScene


class Program:
    DEFAULT_WIN_SIZE = pygame.Vector2(960, 540)

    def __init__(self) -> None:
        Window.set_title("Flappy Bird Clone")
        Window.set_size(self.DEFAULT_WIN_SIZE)
        Display.update_display_from_window()

        Engine.set_scene(MainScene())

    def start(self):
        Engine.start_loop()


if __name__ == "__main__":
    Program().start()
