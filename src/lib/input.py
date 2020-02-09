import pygame
from pygame.locals import (
    K_UP, K_k, K_SPACE, K_w, K_h, K_ESCAPE
)
BUTTON_LEFT = 0
BUTTON_MIDDLE = 1
BUTTON_RIGHT = 2

class InputKey:
    def __init__(self, key_code: int):
        self.held = False
        self.first = False

class InputHandler:
    """Classe para processamento de dados da entrada do jogador."""
    def __init__(self):
        self.keymap = {}
        self.mouse_pos = pygame.Rect(0, 0, 0, 0)

        self.keymap[K_UP] = InputKey(K_UP)
        self.keymap[K_h] = InputKey(K_h)
        self.keymap[K_ESCAPE] = InputKey(K_ESCAPE)
        self.keymap[BUTTON_LEFT] = InputKey(BUTTON_LEFT)
        self.keymap[BUTTON_MIDDLE] = InputKey(BUTTON_MIDDLE)
        self.keymap[BUTTON_RIGHT] = InputKey(BUTTON_RIGHT)

    def process(self):
        # Pegar dados não-processados sobre as teclas
        raw_keymap = pygame.key.get_pressed()
        raw_mouse = pygame.mouse.get_pressed()
        self.mouse_pos.center = pygame.mouse.get_pos()

        # Teclas válidas para cima
        upkeys = raw_keymap[K_UP] or raw_keymap[K_k] or raw_keymap[K_SPACE] or raw_keymap[K_w] or bool(raw_mouse[0])

        # Limpar as variáveis `first`
        self.keymap[K_UP].first = False
        self.keymap[K_h].first = False
        self.keymap[BUTTON_LEFT].first = False
        self.keymap[BUTTON_MIDDLE].first = False
        self.keymap[BUTTON_RIGHT].first = False
        self.keymap[K_ESCAPE].first = False

        # Preencher a lista de variáveis `first`
        if upkeys and not self.keymap[K_UP].held:
            self.keymap[K_UP].first = True
        if raw_keymap[K_h] and not self.keymap[K_h].held:
            self.keymap[K_h].first = True
        if raw_mouse[0] and not self.keymap[BUTTON_LEFT].held:
            self.keymap[BUTTON_LEFT].first = True
        if raw_mouse[1] and not self.keymap[BUTTON_MIDDLE].held:
            self.keymap[BUTTON_MIDDLE].first = True
        if raw_mouse[2] and not self.keymap[BUTTON_RIGHT].held:
            self.keymap[BUTTON_RIGHT].first = True
        if raw_keymap[K_ESCAPE] and not self.keymap[K_ESCAPE].held:
            self.keymap[K_ESCAPE].first = True

        # Atualizar a lista de variáveis `held`
        self.keymap[K_UP].held = upkeys
        self.keymap[K_h].held = raw_keymap[K_h]
        self.keymap[BUTTON_LEFT].held = raw_mouse[0]
        self.keymap[BUTTON_MIDDLE].held = raw_mouse[1]
        self.keymap[BUTTON_RIGHT].held = raw_mouse[2]
        self.keymap[K_ESCAPE].held = raw_keymap[K_ESCAPE]
