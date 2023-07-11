import pygame


class Keyboard:
    keys = {}
    pressed_in_frame = {pygame.KEYDOWN: [], pygame.KEYUP: []}

    @classmethod
    def update(cls, events):
        cls.pressed_in_frame[pygame.KEYDOWN].clear()
        cls.pressed_in_frame[pygame.KEYUP].clear()
        for event in events:
            if event.type == pygame.KEYDOWN:
                cls.keys[event.key] = event
                cls.pressed_in_frame[pygame.KEYDOWN].append(event)
            elif event.type == pygame.KEYUP:
                cls.keys[event.key] = None
                cls.pressed_in_frame[pygame.KEYUP].append(event)

    @classmethod
    def get_pressed(cls, key):
        return cls.get_key_event(key) is not None

    @classmethod
    def get_key_event(cls, key):
        return cls.keys.get(key, None)
