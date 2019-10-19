'''Uma série de objetos utilizados no jogo.'''

class Bird:
    '''O pássaro.'''
    def __init__(self, pos):
        self.pos = list(pos)
        self.animFrame = 0
        self.ySpeed = 0
    pass

class Pipe:
    '''O cano.'''
    pass
