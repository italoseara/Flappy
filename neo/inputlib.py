import pygame
from pygame.locals import *

class PlayerInput:

    '''Classe para processamento de dados da entrada do jogador.'''

    def __init__(self, firstIterate=False):

        '''Inicia as variáveis para as teclas e (opcionalmente) as define já de primeira.

        Argumentos:
        firstIterate -- se irá iterar os valores ao ser criado (padrão: False)'''

        # Direcionais
        self.keyUp = 0

        if firstIterate:
            # (OPCIONAL) Chamar o método iterate() para poder definir os valores.
            self.iterate()

    def iterate(self):

        '''Iriam ser utilizadas três variáveis (NOTHING, HOLD, PRESSED) para indicar o estado das teclas, mas isso acabou ficando muito complicado ("verbose"). Por isso, aqui a explicação:
        0 => NOTHING (nada)
        1 => HELD (segurando)
        2 => PRESSED (pressionado, apenas por 1 frame)'''

        _keyMap = pygame.key.get_pressed()

        if _keyMap[K_UP]:
            if self.keyUp == 2: self.keyUp = 1
            else: self.keyUp = 2
        else: self.keyUp = 0
