
import pygame


class Mouse:
    pos = None
    rel_pos = None
    wheel = None
    in_motion = None
    __pressed_in_frame = None
    pressed_event = None
    __button_index = None

    def __init__(self):
        self.__pressed_in_frame = {}
        
        self.__button_index = {pygame.BUTTON_LEFT:0, pygame.BUTTON_MIDDLE:1, pygame.BUTTON_RIGHT:3}

    def update(self):
        down = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        up = pygame.event.get(pygame.MOUSEBUTTONUP)
        for event in down:
           self.__pressed_in_frame[event.button] = True
        for event in up:
            self.__pressed_in_frame[event.button] = False

    def get_pressed(self, button):
        return pygame.mouse.get_pressed()[self.__button_index[button]]

    def get_pressed_in_frame(self, button):
        return self.__pressed_in_frame.get(button, False)


class KeyBoard:
    pressed_in_frame = None
    
    def __init__(self):
        self.pressed_in_frame = {pygame.KEYDOWN: [], pygame.KEYUP: []}
        self.keys= {}
        # self.key_sequence = []

    def update(self):
        # self.key_sequence.clear()
        self.pressed_in_frame[pygame.KEYDOWN].clear()
        self.pressed_in_frame[pygame.KEYUP].clear()
        
        down = pygame.event.get(pygame.KEYDOWN)
        up = pygame.event.get(pygame.KEYUP)
        
        for event in down:
            self.pressed_in_frame[pygame.KEYDOWN].append(event.key)
            self.keys[event.key] = event
        for event in up:
            self.pressed_in_frame[pygame.KEYUP].append(event.key)
            self.keys[event.key] = None

    def get_pressed(self, key):
        return self.get_key_event(key) is not None

    def get_key_event(self, key):
        return self.keys.get(key, None)
    
    def get_pressed_in_frame(self, key):
        return self.pressed_in_frame[key]


class Devices:
    def __init__(self):
        self.mouse = Mouse()
        self.keyboard = KeyBoard()

    def update(self):
        self.mouse.update()
        self.keyboard.update()