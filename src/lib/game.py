"""Arquivo com os objetos específicos ao jogo."""

from lib.obj import Object
from lib.data import Vector2D
from lib.maths import gameobject_hitbox, gameobject_size
import pygame

class Player(Object):
    
    def __init__(self, pos, frames, linked_game):
        """Inicia o jogador."""
        self.setup(pos, frames, linked_game)
        self.speed = Vector2D(0, 0)
        self.angle = 0
        self.angle_target = 0
        self.health = 0
        self.fixed_hitbox = gameobject_hitbox(self)
        self.jump_counter = 0
        self.animation_timer = 0

    def process(self):
        pinput = self.linked_game.input

        # Adicionar ao jump_counter
        self.jump_counter += 1

        if pinput.keymap[pygame.K_UP].first:
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

        self.pos.y += self.speed.y
        if self.linked_game.state != 0:
            self.speed.y += self.linked_game.gravity

        # Isso não é usado no código do pássaro, mas talvez seja útil colocar.
        self.speed.x = self.linked_game.speed

        # "Capar" a velocidade vertical se o pássaro atingir o topo da tela enquanto estiver pulando.
        if self.pos.y < 0:
            self.pos.y = 0
            self.speed.y = 0

        # Deixar o pássaro entalado pouco depois da parte de baixo da tela se ele chegar lá.
        if self.pos.y > (self.linked_game.winsize[1] + gameobject_size(self)[1]):
            self.pos.y = (self.linked_game.winsize[1] + gameobject_size(self)[1])
            self.speed.y = 0
        # Previne um bug estranho: "se o jogador cair demais, ele volta para o topo da tela"

        elif (self.pos.y >= self.linked_game.ground_pos - self.fixed_hitbox[3]
              and self.linked_game.state == 1):
            self.pos.y = self.linked_game.ground_pos - self.fixed_hitbox[3]
            self.speed.y = 0
            self.linked_game.state = 2
            self.speed.y = -8

    def render(self):

        if self.animation_timer == 8:
            self.frames.current_index += 1
            self.animation_timer = 0

        if self.frames.current_index >= 4:
            self.frames.current_index = 0

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
        old_center = (self.pos.x + 15, self.pos.y + 15)
        new_image = pygame.transform.rotate(
            self.frames.current_frame, self.angle
        )
        rect = new_image.get_rect()
        rect.center = old_center

        return (new_image, rect)

class Pipe(Object):
    """Código principal do cano."""

    def __init__(self, pos, frames, linked_game=None, speed: float = 1.0):
        self.setup(pos, frames, linked_game)
        self.speed = speed
        self.has_scored = False # Usado no código principal para ver se o jogador já passou desse cano e já pegou a pontuação.

    def process(self):
        """Processamento padrão dos canos.

        A cada frame, o cano vai um pouco à esquerda, dependendo do valor de sua velocidade."""
        self.pos.x -= self.speed

class Tile(Object):
    """Código principal dos Tiles (chão e fundo)."""

    def __init__(self, pos, frames, linked_game=None, speed: float = 1.0, **kwargs):
        """O construtor da classe. Ele inicia o tile.

        speed -- A velocidade de movimento do tile.
        kwargs -- Alguns argumentos extras. Funcionalidades que utilizam isso não se localizam aqui.
        """
        self.setup(pos, frames, linked_game)
        self.speed = speed
        self.kwargs = kwargs
