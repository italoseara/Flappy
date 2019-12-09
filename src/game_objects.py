from base_classes import GameObject, Vector2D
from functions import gameobject_hitbox, gameobject_size
import pygame

"""Arquivo com os objetos que constroem o jogo."""

class Player(GameObject):
    """Objeto do jogador (pássaro)."""

    def __init__(self, pos=(0, 0), frame_list=[], linked_game=None):
        """Inicia o jogador.

        Passos:
            - Chama a função _setup para iniciar alguns valores
            - Define o frame atual da animação
            - Inicia um vetor para a velocidade
            - Define o ângulo inicial
            - Define o ângulo para onde o pássaro deve lentamente girar.
            - Define o estado de saúde*
                * O estado de saúde pode ser:
                - 0 => Estático (na tela de início do jogo)
                - 1 => Vivo (durante o jogo)
                - 2 => Morto (entrou em colisão com algum obstáculo ou o chão)
        """
        self._setup(pos, frame_list, linked_game)
        self.speed = Vector2D(0, 0)
        self.angle = 0
        self.angle_target = 0
        self.health = 0
        self.fixed_hitbox = gameobject_hitbox(self)
        self.jump_counter = 0
        self.animation_timer = 0

    def _process(self):

        pinput = self.linked_game.input

        # Adicionar ao jump_counter
        self.jump_counter += 1

        if pinput.key_up[1]:
            # Ao apertar a seta para cima:

            # Iniciar o jogo se ele ainda não tiver sido iniciado.
            if self.linked_game.state == 0:
                self.linked_game.state = 1

            # Reiniciar se o jogador estiver morto.
            elif self.linked_game.state == 2:
                self.linked_game.timer = 0

            # Pular se o jogo já tiver começado (incluindo logo quando o jogo iniciar)
            if self.linked_game.state in {0, 1}:
                self.speed.y = -8
                self.jump_counter = 0

        # MOVIMENTO ###########################

        self.y += self.speed.y
        if self.linked_game.state != 0:
            self.speed.y += self.linked_game.gravity

        # Isso não é usado no código do pássaro, mas talvez seja útil colocar.
        self.speed.x = self.linked_game.speed

        # "Capar" a velocidade vertical se o pássaro atingir o topo da tela enquanto estiver pulando.
        if self.y < 0:
            self.y = 0
            self.speed.y = 0

        # Deixar o pássaro entalado pouco depois da parte de baixo da tela se ele chegar lá.
        if self.y > (self.linked_game.winsize[1] + gameobject_size(self)[1]):
            self.y = (self.linked_game.winsize[1] + gameobject_size(self)[1])
            self.speed.y = 0
        # Previne um bug estranho: "se o jogador cair demais, ele volta para o topo da tela"

        elif (self.y >= self.linked_game.ground_pos - self.fixed_hitbox[3]
              and self.linked_game.state == 1):
            self.y = self.linked_game.ground_pos - self.fixed_hitbox[3]
            self.speed.y = 0
            self.linked_game.state = 2
            self.speed.y = -8

    def compile_render(self):
        """Compila e retorna uma tupla com o frame a ser renderizado e um retângulo de posição."""

        # TODO: Documentar essa parte melhor.

        if self.animation_timer == 8:
            self.current_frame += 1
            self.animation_timer = 0

        if self.current_frame >= 4:
            self.current_frame = 0

        if self.linked_game.state != 0:

            # Achar ângulo
            if self.jump_counter < 30:
                self.angle_target = 30
            else:
                self.angle_target = -45

            # Girar o pássaro
            self.angle += (self.angle_target - self.angle) * 0.15
            self.angle_target = (self.angle_target + 360) % 360

        # Atualizar a imagem para poder retornar
        old_center = (self.x + 15, self.y + 15)
        new_image = pygame.transform.rotate(
            self.frame_list[self.current_frame], self.angle
        )
        rect = new_image.get_rect()
        rect.center = old_center

        return (new_image, rect)

class Pipe(GameObject):
    """Código principal do cano."""

    def __init__(self, pos=(0, 0), frame_list=[], speed=1, linked_game=None):
        self._setup(pos, frame_list, linked_game)
        self.speed = speed
        self.has_scored = False # Usado no código principal para ver se o jogador já passou desse cano e já pegou a pontuação.

    def _process(self):
        """Processamento padrão dos canos.

        A cada frame, o cano vai um pouco à esquerda, dependendo do valor de sua velocidade."""
        self.x += -self.speed

class Tile(GameObject):
    """Código principal dos Tiles (chão e fundo)."""

    # TODO: Documentar essa parte melhor - principalmente os kwargs.

    def __init__(self, pos=(0, 0), frame_list=[], linked_game=None, speed=1, **kwargs):
        """O construtor da classe. Ele inicia o tile.

        speed -- A velocidade de movimento do tile.
        kwargs -- Alguns argumentos extras. Funcionalidades que utilizam isso não se localizam aqui.
        """
        self._setup(pos, frame_list, linked_game)
        self.speed = speed
        self.kwargs = kwargs
