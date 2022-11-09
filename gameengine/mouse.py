import pygame


class Mouse:
    pos = (0, 0)
    _default_pressed_event = [False, False, False]
    pressed_event = list(_default_pressed_event)
    pressed = list(_default_pressed_event)

    @classmethod
    def update(cls, gameengine):
        cls.pressed_event = list(cls._default_pressed_event)
        for event in gameengine.events:
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                button = None
                if event.button in (
                    pygame.BUTTON_LEFT,
                    pygame.BUTTON_MIDDLE,
                    pygame.BUTTON_RIGHT,
                ):
                    button = event.button
                if button is not None:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        cls.pressed[event.button - 1] = True
                        cls.pressed_event[event.button - 1] = True
                    else:
                        cls.pressed[event.button - 1] = False
            if event.type == pygame.MOUSEMOTION:
                cls.pos = event.pos

    @classmethod
    def get_pressed(cls, pygame_button):
        return cls.pressed[pygame_button - 1]

    @classmethod
    def get_pressed_event(cls, pygame_button):
        return cls.pressed_event[pygame_button - 1]
