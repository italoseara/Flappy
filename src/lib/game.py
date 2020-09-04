from .obj import Object
from .data import Vector2D
from .maths import gameobject_hitbox, gameobject_size
from math import sin
import pygame

class Player(Object):
    
    def __init__(self, pos, frames, d):
        """Inicia o jogador."""
        self.setup(pos, frames, d)
        self.speed = Vector2D(0, 0)
        self.angle = 0
        self.angle_target = 0
        self.health = 0
        self.fixed_hitbox = gameobject_hitbox(self)
        self.jump_counter = 0
        self.animation_id = 0
        self.animation_timer_limit = 0
        self.animation_timer = 0

    def process(self):
        pinput = self.d.input

        # Adicionar ao jump_counter
        self.jump_counter += 1

        if pinput.keymap[pygame.K_UP].first:
            # Ao apertar a seta para cima:

            # Iniciar o jogo se ele ainda não tiver sido iniciado.
            if self.d.game_state == 0:
                self.d.game_state = 1

            # Pular se o jogo já tiver começado (incluindo logo quando o jogo iniciar)
            if self.d.game_state in {0, 1}:
                self.speed.y = -8
                self.jump_counter = 0

        # MOVIMENTO ###########################

        self.pos.y += self.speed.y
        if self.d.game_state == 0:
            self.speed.y = 0
            self.pos.y += sin(self.d.timer / 10)
        else:
            self.speed.y += self.d.cfg.GRAVITY

        # "Capar" a velocidade vertical se o pássaro atingir o topo da tela enquanto estiver pulando.
        if self.pos.y < 0:
            self.pos.y = 0
            self.speed.y = 0

        # Deixar o pássaro entalado pouco depois da parte de baixo da tela se ele chegar lá.
        # Isso previne um bug estranho: "se o jogador cair demais, ele volta para o topo da tela"
        if self.pos.y > (self.d.cfg.WINSIZE[1] + gameobject_size(self)[1]):
            self.pos.y = (self.d.cfg.WINSIZE[1] + gameobject_size(self)[1])
            self.speed.y = 0

        elif (self.pos.y >= self.d.cfg.GROUND_POS - self.fixed_hitbox[3]
              and self.d.game_state == 1):
            self.pos.y = self.d.cfg.GROUND_POS - self.fixed_hitbox[3]
            self.d.game_state = 2
            self.speed.y = -8

        if self.animation_id == 0:
            # Introdução (voando sem pular)
            self.animation_timer_limit = 8
        elif self.animation_id == 1:
            # Transição para parar as asas (quando morrer)
            self.animation_timer_limit = 8
            if self.frames.current_index == 0:
                self.animation_id = 2
        elif self.animation_id == 2:
            # Asas paradas
            self.animation_timer_limit = None

        if self.animation_id != None:
            self.animation_timer += 1

    def render(self):

        if self.animation_timer == self.animation_timer_limit:
            self.frames.current_index += 1
            if self.frames.current_index >= len(self.frames.frame_list):
                self.frames.current_index = 0
            self.animation_timer = 0

        if self.d.game_state != 0:
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

    def __init__(self, pos, frames, d=None, speed: float = 1.0):
        self.setup(pos, frames, d)
        self.speed = speed
        self.has_scored = False # Usado no código principal para ver se o jogador já passou desse cano e já pegou a pontuação.

    def process(self):
        """Processamento padrão dos canos.

        A cada frame, o cano vai um pouco à esquerda, dependendo do valor de sua velocidade."""
        self.pos.x -= self.speed
        
class Tile(Object):
    """Código principal dos Tiles (chão e fundo)."""

    def __init__(self, pos, frames, d, speed=1.0, parallax_coeff=1.0):
        """O construtor da classe. Ele inicia o tile.

        speed -- A velocidade de movimento do tile.
        """
        self.setup(pos, frames, d)
        self.speed = float(speed)
        self.parallax_coeff = float(parallax_coeff)
