from pygame import Rect, mouse, key
from pygame.locals import (
    K_UP, K_k, K_SPACE, K_w
)

class PlayerInput:
    """Classe para processamento de dados da entrada do jogador."""

    def __init__(self, first_iterate=False):
        """Inicia as variáveis para as teclas e (opcionalmente) as define já de primeira.

        Argumentos:
        first_iterate -- se irá atualizar as variáveis de input logo que os valores forem criados (padrão: False)"""

        # Teclas simuladas (uma tecla pode ser ativada por várias outras, tipo cima & espaço)
        UPKEYS = False

        # Direcionais
        self.key_up = [False, False]

        # Mouse
        self.mouse = Rect(0, 0, 0, 0)
        self.mouse_click_left = [False, False]
        self.mouse_click_middle = [False, False]
        self.mouse_click_right = [False, False]

        if first_iterate:
            self.process()

    def process(self):
        """Define o valor das variáveis de tecla. Cada variável de tecla é uma lista de dois elementos:
        EL #0 => Held (segurando)
        EL #1 => Pressed (pressionado, apenas por 1 frame)"""

        # Posição do Mouse
        self.mouse.center = mouse.get_pos()

        # Obter dados "crus" de input
        _key_map = key.get_pressed()
        _mouse_click = mouse.get_pressed()

        # Atualizar variáveis de simulação de tecla.
        UPKEYS = (
            _key_map[K_UP]
            or _key_map[K_k]
            or _key_map[K_SPACE]
            or bool(_mouse_click[0])
            or _key_map[K_w]
        )

        # Limpar a lista de teclas pressionadas
        self.key_up[1] = False
        self.mouse_click_left[1] = False
        self.mouse_click_middle[1] = False
        self.mouse_click_right[1] = False

        # Preencher a lista de teclas pressionadas
        if UPKEYS and (not self.key_up[0]):
            self.key_up[1] = True
        if _mouse_click[0] and (not self.mouse_click_left[1]):
            self.mouse_click_left[1] = True
        if _mouse_click[1] and (not self.mouse_click_middle[1]):
            self.mouse_click_middle[1] = True
        if _mouse_click[2] and (not self.mouse_click_right[1]):
            self.mouse_click_right[1] = True

        # Limpar/preencher a lista de teclas seguradas
        self.key_up[0] = UPKEYS
        (
            self.mouse_click_left[0],
            self.mouse_click_middle[0],
            self.mouse_click_right[0],
        ) = [bool(x) for x in _mouse_click]
