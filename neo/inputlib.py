import pygame
from pygame.locals import *

class PlayerInput:

    '''Classe para processamento de dados da entrada do jogador.'''

    def __init__(self, firstIterate=False):

        '''Inicia as variáveis para as teclas e (opcionalmente) as define já de primeira.

        Argumentos:
        firstIterate -- se irá iterar os valores ao ser criado (padrão: False)'''

        # Direcionais
        self.keyUp = [False, False]

        if firstIterate:
            # (OPCIONAL) Chamar o método iterate() para poder definir os valores.
            self.iterate()

    def iterate(self):

        '''Define o valor das variáveis de tecla. Cada variável de tecla é uma lista de dois elementos:
        EL #0 => Held (segurando)
        EL #1 => Pressed (pressionado, apenas por 1 frame)'''
        #'''Iriam ser utilizadas três variáveis (NOTHING, HOLD, PRESSED) para indicar o estado das teclas, mas isso acabou ficando muito complicado ("verbose"). Por isso, aqui a explicação:
        #0 => NOTHING (nada)
        #1 => HELD (segurando)
        #2 => PRESSED (pressionado, apenas por 1 frame)'''

        # Obter a lista de input
        _keyMap = pygame.key.get_pressed()
        
        # Limpar a lista de teclas pressionadas
        self.keyUp[1] = False

        # Preencher a lista de teclas pressionadas
        if _keyMap[K_UP] and (not self.keyUp[0]): self.keyUp[1] = True

        # Limpar/preencher a lista de teclas seguradas
        self.keyUp[0] = _keyMap[K_UP]
