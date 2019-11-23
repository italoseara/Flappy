#!/usr/bin/env python3

"""Classes úteis para o jogo."""

import pygame


class Logger:
    """Sistema de logging simples."""

    def __init__(self, enabled=True):

        self.enabled = enabled

    def print(self, *args, **kwargs):
        """Uma interface para imprimir coisas na tela com o sistema de logging."""

        PREFIX = "\033[34m(L)\033[m"
        print(PREFIX, *args, **kwargs)


class GameObject:
    """A base para todos os elementos interativos no jogo.
    Contém um conjunto de funções e atributos padrões.

    Todos os objetos do jogo devem derivar desta classe.
    """

    def __init__(self, pos=(0, 0), frame_list=[0], linked_game=None):
        """Inicia a classe.
        
        A substituição desta função é recomendada, mas lembre-se de chamar a função self._setup logo no início dela.

        Atributos:
        pos -- A posição do objeto.
        frame_list -- A lista de frames, usada principalmente em animações.
        linked_game -- O jogo que está conectado. É opcional, mas recomendado para facilitar a conexão entre o jogo e objetos.
        """
        self._setup(pos, frame_list, linked_game)

    def _setup(self, pos=(0, 0), frame_list=[0], linked_game=None):
        """Uma função para iniciar a classe.
        
        Por padrão, ela é chamada na função __init__;
        Ela foi movida para um lugar separado para deixar a função __init__ fácil de ser substituída sem muitas complicações. Basta chamar esta função.

        A substituição desta função não é recomendada.
        """
        self.pos = pos
        self.frame_list = frame_list
        self.current_frame = 0
        self.linked_game = linked_game

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, value):
        self.x, self.y = value

    def _process(self):
        """Função de iteração do objeto.

        Foi feita com o intuito de agrupar código relacionado ao objeto para ser chamado uma vez por frame.

        A substituição desta função é recomendada.
        """
        pass

    def compile_render(self):
        """Compila e retorna uma tupla com o frame a ser renderizado e um retângulo de posição.

        A substituição desta função é opcional.
        """
        return self.frame_list[self.current_frame], self.pos


class Vector2D:
    """Um vetor em duas dimensões.

    Inspirado no Godot.
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if type(value) not in {int, float}:
            raise ValueError(f"O valor {value} não é nem int nem float")
        else:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if type(value) not in {int, float}:
            raise ValueError(f"O valor {value} não é nem int nem float")
        else:
            self._y = value

    def normalize(self):
        raise NotImplementedError


class Game:
    """O objeto principal do jogo."""

    def __init__(self):
        """Prepara o jogo.
        
        A substituição desta função é recomendada, mas lembre-se de chamar a função self._setup logo no início dela.
        """
        self._setup(pos, frame_list, linked_game)

    def _setup(self):
        """Uma função para iniciar a classe do jogo.
        
        Por padrão, ela é chamada na função __init__;
        Ela foi movida para um lugar separado para deixar a função __init__ fácil de ser substituída sem muitas complicações. Basta chamar esta função.

        A substituição desta função não é recomendada.
        """
        self.img = (
            {}
        )  # Cria um dicionário vazio para carregar as imagens. Essas imagens devem ser carregadas utilizando self._load_resources e self._load_a_resource()

    def _load_resources(self):
        pass

    def _load_a_resource(self, key, relative_path, force=False):
        """Carrega um recurso e adiciona-o ao dicionário em self.img.

        relative_path -- Uma string com o caminho do arquivo, relativo ao arquivo atual (main.py). Aceita também tuplas, listas e sets com strings dentro.
        key -- O nome da chave a adicionar no dicionário self.img.
        force -- Sempre força a ação, ignorando os erros mencionados acima.
        """

        image = None

        # Verifica se relative_path é uma tupla/lista/set
        if type(relative_path) in {tuple, list, set}:
            image = []
            for string in relative_path:
                if type(string) != str:
                    raise ValueError(
                        f"{string.__repr__()} @ {relative_path} não é uma string."
                    )
                else:
                    image.append(pygame.image.load(string))
        elif type(relative_path) == str:
            image = pygame.image.load(relative_path)
        else:
            raise ValueError(
                f"{relative_path.__repr__()} não é tupla, lista, set ou string."
            )

        # Se a key já existir
        if key in self.img:
            if force:
                self.logger.print(
                    f"[Force] Carregado {relative_path} na image key {key.__repr__()}."
                )
            else:
                raise KeyError(
                    f"A chave {key.__repr__()} já possui conteúdo (tentou carregar {relative_path})"
                )

        # Se a key não existir
        else:
            self.img[key] = image
            self.logger.print(
                f"Carregado {relative_path} na nova image key {key.__repr__()}"
            )
