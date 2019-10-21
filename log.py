class Log:

    '''Uma classe para mostrar informações (opcionais).'''

    def __init__(self, enabled=True):
        self.enabled = enabled
    
    def print(self, *args, **kwargs):
        print('(L)', end=' ')
        print(*args, **kwargs)
