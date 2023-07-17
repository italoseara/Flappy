import pygame

from .devices import Devices
from .scene import BaseScene

pygame.init()


class TimeManager:
    target_framerate = None
    delta = None
    clock = None

    def __init__(self, target_framerate):
        self.set_framerate(target_framerate)
        self.delta = 1 / target_framerate

        self.clock = pygame.time.Clock()

    def set_framerate(self, new_framerate):
        self.target_framerate = new_framerate

    def update(self):
        self.delta = self.clock.tick(self.target_framerate)/1000


class EventsManager:
    uncaught_events = None

    def update(self):
        self.uncaught_events = pygame.event.get()


class DefaultScene(BaseScene): pass


class Program:
    scene = None

    request_quit = False

    def __init__(self, window, framerate=30):
        self.window = window
        self.time = TimeManager(framerate)
        self.devices = Devices()
        self.event = EventsManager()
        
        self.scene = DefaultScene()

    def set_scene(self, new_scene):
        self.scene = new_scene

    def update(self):
        self.devices.update()
        self.event.update()
        
        self.scene.update()
        
        self.time.process()
