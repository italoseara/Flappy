#!/usr/bin/env python3

# Clone de Flappy Bird
# Autores: ItaloDoArbusto, YohananDiamond
# Repositório: https://github.com/ItaloDoArbusto/Flappy

# TODO: Encontrei um bug em que, se o jogador cair demais, ele volta para o topo da tela. Tenho que consertar isso ainda.

# INICIALIZAÇÃO GERAL ############################

# Imports Iniciais
import pygame
from pygame.locals import *
from random import randint

# Importar módulos locais
from game_objects import *
from base_classes import *
from functions import *
from pinput import PlayerInput


def main(argv):

    # Iniciar o pygame
    pygame.init()

    # Criar e iniciar o jogo
    game = FlappyGame(game_speed=3, debug=False)
    game.runtime()


# PARTE PRINCIPAL ##################################


class FlappyGame(Game):
    """O código principal do jogo."""

    def __init__(self, game_speed, debug):
        """Organiza as variáveis principais do jogo e carrega alguns recursos."""

        # Criar objetos relacionados
        self.logger = Logger(enabled=debug)
        self.input = PlayerInput()

        # Carregar alguns recursos
        self._setup()
        self._load_resources()

        # Criar algumas variáveis
        self.timer = 0
        # self.timer2 = 0
        self.clock = pygame.time.Clock()
        self.speed = game_speed
        self.state = 0
        self.debug = debug
        self.score = 0

    def _load_resources(self):
        """Carrega os recursos do jogo."""

        # Gráficos
        load = self._load_a_resource
        load("icon", "img/icon.bmp")
        load("floor", "img/floor.png")
        load("bg", "img/background.png")
        load(
            "bird",
            [
                "img/bird_f0.png",
                "img/bird_f1.png",
                "img/bird_f2.png",
                "img/bird_f1.png",  # TODO: Analisar isso aqui depois.
                "img/bird_fDead.png",
            ],
        )
        load("tube_top", "img/tube_top.png")
        load("tube_bottom", "img/tube_bottom.png")
        load("tip", "img/tip.png")
        load("game_over", "img/game_over.png")
        load("pause_button", "img/pause.png")
        load("menu", "img/menu.png")

        # Fontes utilizadas
        self.score_font = pygame.font.SysFont(
            "Ubuntu Mono, Cascadia Code, Consolas, Fixedsys", 20
        )

    def runtime(self):
        """Código principal do jogo."""

        # Constantes locais ao jogo
        WINSIZE = (960, 540)
        FRAMERATE = 60
        COLOR_BACKGROUND = (115, 200, 215)
        INIT_POSITION = (
            WINSIZE[0] / 2 - image_size(self.img["bird"][0])[0] / 2,
            WINSIZE[1] / 2 - image_size(self.img["bird"][0])[1] / 2,
        )

        # Definir a janela
        screen = pygame.display.set_mode(WINSIZE)  # Criar Janela
        pygame.display.set_caption("Flappy Bird")  # Definir Título
        pygame.display.set_icon(self.img["icon"])  # Definir Ícone

        class var:
            """Uma subclasse que contém algumas variáveis para o jogo.
            Elas estão aqui porque estão relacionadas a algum objeto ou não são constantes.
            Isso pode ser utilizado também quando se quer criar uma variável que funcione em todos os frames, mas quando está dentro do loop principal (não tão recomendado)."""

            pipe_spawn_counter = 0  # Um contador com o tempo de spawn.

        # CRIAR OBJETOS #######################

        # Botão de Pause
        # rect = self.img['pause_button'].get_rect()
        # rect.center = (30, 30)
        # rectangle = self.img['pause_button'].get_rect().size
        # TODO: Fazer botão de pause

        # Criar objetos principais
        player = Player(INIT_POSITION, self.img["bird"], linked_game=self)

        # Criar objetos do cenário
        floor_tiles = []
        pipes_list = []
        background_tiles = []

        # Variáveis para o início do jogo
        running = True
        self.state = 0
        self.gravity = 0.5
        self.ground_pos = 476

        # FUNÇÕES #############################

        def make_tiles():
            """Prepara os tiles do jogo."""
            return (
                # Tiles do Chão (floor)
                [
                    Tile((0, self.ground_pos), [self.img["floor"]], factor=1),
                    Tile((1600, self.ground_pos), [self.img["floor"]], factor=1),
                ],
                # Tiles do Fundo (background)
                [
                    Tile((0, 0), [self.img["bg"]], factor=0.5),
                    Tile((1600, 0), [self.img["bg"]], factor=0.5),
                ],
            )

        floor_tiles, bg_tiles = (
            [],
            [],
        )  # Um patch preguiçoso que cria as listas de tiles antes de preenchê-las para poder fazer o código mais abaixo funcionar.

        # LOOP PRINCIPAL (FRAMES) #############

        while running:

            # Variáveis atualizadas no início do frame
            var.pipe_spawn_delay = 200 / self.speed

            # Limitar a quantidade de frames.
            self.clock.tick(FRAMERATE)

            # INPUT & FÍSICA ##################

            # Atualizar as teclas e entradas de mouse pressionadas.
            self.input.iterate()

            # NOTE: O código do pulo foi movido para a classe Player em game_objects.py, assim como o de iniciar o jogo.

            # Atualizar o jogador
            player._process()

            # Código do jogo iniciado
            if self.state == 1:

                # Diminuir do contador de spawn de canos
                var.pipe_spawn_counter -= 1

                # Spawnar dois canos (um em cima e um em baixo) quando o counter acabar.
                if var.pipe_spawn_counter <= 0:

                    # Achar valor aleatório para o spawn do cano.
                    height = randint(-210, -40)
                    spacing = 130
                    bottom_pipe_height = (
                        height + image_size(self.img["tube_top"])[1] + spacing
                    )

                    # Criar o cano de cima
                    new_pipe_top = Pipe(
                        (WINSIZE[0], height), [self.img["tube_top"]], self.speed
                    )
                    pipes_list.append(new_pipe_top)

                    # Criar o cano de baixo
                    new_pipe_bottom = Pipe(
                        (WINSIZE[0], bottom_pipe_height),
                        [self.img["tube_bottom"]],
                        self.speed,
                    )
                    pipes_list.append(new_pipe_bottom)

                    # Resetar o counter
                    var.pipe_spawn_counter = var.pipe_spawn_delay

                # Iterar os canos
                for (pipe_index, pipe) in enumerate(pipes_list):

                    pipe._process() # Atualizar os canos
                    pipe_hitbox = gameobject_hitbox(pipe) # Criar hitbox do cano

                    # Morte pela colisão entre jogador e cano
                    if pipe_hitbox.colliderect(gameobject_hitbox(player)):
                        self.state = 2
                        player.speed.y = -8

                    # Pontos ao passar pelo cano
                    # Parte do código está na classe do pipe.
                    if player.x > pipe.x + pipe_hitbox[3]:
                        if not pipe.has_scored:
                            self.score += 1
                            pipe.has_scored = True

                    # Despawnar o cano quando ele sair da esquerda da tela.
                    if pipe.x < (0 - gameobject_size(pipe)[0]):
                        del pipes_list[pipe_index]

            # Iterar logo tudo
            # Colocar isso antes da preparação das listas do primeiro frame para que o jogo não comece com os itens se mexendo já para trás.
            if self.state in {0, 1}:
                for tile_list in (floor_tiles, bg_tiles):
                    for tile in tile_list:
                        # Mexer na velocidade
                        # Parallax para isso pode ser definido pela key 'factor' no atributo 'kwargs' dos objetos iterados aqui.
                        tile.x -= self.speed * tile.kwargs["factor"]
                        # Mover o tile para a direita se ele já saiu completamente da tela.
                        if tile.x < (0 - gameobject_size(tile)[0]):
                            tile.x = WINSIZE[0]

            # Preparar as listas de floor e background no primeiro do jogo.
            # Funciona também com resets - basta definir o valor do timer para 0.
            if self.timer == 0:
                floor_tiles, bg_tiles = make_tiles()
                pipes_list = []
                self.state = 0
                player.angle_target = player.angle = 0
                player.speed.y = 0
                player.pos = INIT_POSITION

            # RENDERIZAÇÃO ####################

            # Preencher o fundo (céu)
            screen.fill(COLOR_BACKGROUND)

            # Renderizar todos os GameObject's existentes no jogo.
            for object_ in bg_tiles + pipes_list + floor_tiles:
                gameobject_render(object_, screen)
            gameobject_render(player, screen)

            # Mostrar a dica inicial
            # TODO: Fazer um posicionamento melhor (cálculos de centralização, talvez rect.center)
            if self.state == 0:
                screen.blit(self.img["tip"], (80, 0))

            # Mostrar o botão de pause
            # FIXME: Fazer esse botão realmente funcionar. Parece estar errado.
            # screen.blit(self.img['pause_button'], (0, 0)) # tinha um rect no lugar de (0, 0), mas eu não sei pq.

            # Hitboxes
            if self.debug:
                drect = pygame.draw.rect
                HITBOX_COLOR = (255, 0, 0)
                HITBOX_WIDTH = 2
                for pipe in pipes_list:
                    drect(screen, HITBOX_COLOR, gameobject_hitbox(pipe), HITBOX_WIDTH)
                drect(
                    screen, HITBOX_COLOR, (0, self.ground_pos, *WINSIZE), HITBOX_WIDTH
                )

            # Score & FPS
            debug_text = f"Score: {self.score}; FPS: {int(self.clock.get_fps())}"
            text_pos = (15, 10)
            fps_text = self.score_font.render(debug_text, True, pygame.Color("white"))
            screen.blit(fps_text, text_pos)

            # Tela de Game over
            if self.state == 2:
                screen.blit(
                    self.img["game_over"], (100, 0)
                )  # TODO: Cálculo de posicionamento melhor

            # Atualizar a Tela
            pygame.display.update()

            # POST-PROCESSING #################

            # Processamento de eventos
            for event in pygame.event.get():
                # Sair pelo comando sair da janela
                # (Botão X no canto, Alt+F4 etc.)
                if event.type == QUIT:
                    running = False

            # Adicionar 1 ao timer
            self.timer += 1
            # self.timer2 += 1
            # if self.timer2 > 8:
            # self.timer2 = 0


if __name__ == "__main__":
    from sys import argv

    main(argv)
