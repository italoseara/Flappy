import pygame
from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.window import Window


class Program:
    DEFAULT_WIN_SIZE = pygame.Vector2(960, 540)

    def __init__(self) -> None:
        Window.set_title("Flappy Bird Clone")
        Window.set_size(self.DEFAULT_WIN_SIZE)
        Display.update_display_from_window()

    def start(self):
        Engine.start_loop()


if __name__ == "__main__":
    Program().start()
