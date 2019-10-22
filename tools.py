from pygame import Rect

'''Algumas ferramentas úteis para o jogo.'''

def imgsize(image):
    
    '''Obtém o tamanho de uma imagem.'''
    return image.get_rect().size

def objsize(obj):

    '''Obtém o tamanho de um objeto.'''

    #assert type(object).__name__ == 'GameObject'
    return obj.frames[0].get_rect().size

def gethitbox(obj):

    '''Obtém um retângulo localizado da hitbox da imagem.'''

    #assert type(object).__name__ == 'GameObject'
    return Rect(tuple(obj.pos) + imgsize(obj.frames[0]))

class Logger:

    '''Uma classe para mostrar informações (opcionais).'''

    def __init__(self, enabled=True):
        self.enabled = enabled
    
    def print(self, *args, **kwargs):
        print('(L)', end=' ')
        print(*args, **kwargs)
