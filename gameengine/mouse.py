import pygame


class Mouse:
    pos = pygame.Vector2(0, 0)
    rel_pos = pygame.Vector2(0, 0)
    wheel = pygame.Vector2(0, 0)
    in_motion = False
    pressed_event = {}
    pressed = {}

    @classmethod
    def update(cls, events):
        cls.pressed_event.clear()
        cls.wheel.xy = (0, 0)
        cls.in_motion = False
        for event in events:
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
                        cls.pressed[event.button] = True
                        cls.pressed_event[event.button] = True
                    else:
                        cls.pressed[event.button] = False
            if event.type == pygame.MOUSEMOTION:
                cls.pos.xy = event.pos
                cls.rel_pos.xy = event.rel
                cls.in_motion = True
            if event.type == pygame.MOUSEWHEEL:
                cls.wheel.xy = (event.x, event.y)

    @classmethod
    def get_pressed(cls, pygame_button):
        return cls.pressed.get(pygame_button, False)

    @classmethod
    def get_pressed_in_frame(cls, pygame_button):
        return cls.pressed_event.get(pygame_button, False)
