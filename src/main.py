# INICIALIZAÇÃO GERAL ############################

# Imports Iniciais
import pygame
from pygame.locals import *
from random import randint

# Importar módulos locais
from lib.game import *
from lib.input import InputHandler, BUTTON_LEFT, BUTTON_MIDDLE, BUTTON_RIGHT
from lib.obj import *
from lib.data import *
from lib.maths import *

def main(argv):
    """Cria uma instância do jogo e a inicia."""
    pygame.init()
    game = FlappyGame(
        RESOURCES,
        game_speed=3,
        debug=False,
    )
    game.runtime()

# VARIÁVEIS INICIAIS ###############################

RESOURCES = [
    ("icon", "res/icon.bmp"),
    ("floor", "res/floor.png"),
    ("bg", "res/background.png"),
    ("bird", "res/bird_f0.png"),
    ("tube_top", "res/tube_top.png"),
    ("tube_bottom", "res/tube_bottom.png"),
    ("tip", "res/tip.png"),
    ("game_over", "res/game_over.png"),
    ("pause_button", "res/pause.png"),
    ("menu", "res/menu.png"),
]

WINSIZE = (960, 540)

# PARTE PRINCIPAL ##################################

class FlappyGame(Game):
    """O código principal do jogo."""

    def __init__(self, resource_data: list, game_speed, debug):
        """Organiza as variáveis principais do jogo e carrega os recursos."""

        # Iniciar a classe
        self.setup(resource_data)

        self.score_font = pygame.font.SysFont(
            "Ubuntu Mono, Cascadia Code, Consolas, Fixedsys", 20
        )

        # Criar objetos relacionados
        self.input = InputHandler()
        self.clock = pygame.time.Clock()

        # Criar algumas variáveis
        self.winsize = WINSIZE
        self.timer = 0
        self.state = 0
        self.score = 0
        self.speed = game_speed
        self.debug = debug

    def runtime(self):
        """Código principal do jogo."""

        # "Atalhos"
        WINSIZE = self.winsize

        # Constantes locais ao jogo
        FRAMERATE = 60
        COLOR_BACKGROUND = (115, 200, 215)
        INIT_POSITION = (
            WINSIZE[0] / 2 - image_size(self.res["bird"])[0] / 2,
            WINSIZE[1] / 2 - image_size(self.res["bird"])[1] / 2,
        )

        # Definir a janela
        screen = pygame.display.set_mode(WINSIZE) # Criar Janela
        pygame.display.set_caption("Flappy: {}x{}".format(*WINSIZE)) # Definir Título
        pygame.display.set_icon(self.res["icon"]) # Definir Ícone

        class var:
            """Uma subclasse que contém algumas variáveis para o jogo.
            Elas estão aqui porque estão relacionadas a algum objeto ou não são constantes.
            Isso pode ser utilizado também quando se quer criar uma variável que funcione em todos os frames, mas quando está dentro do loop principal (não tão recomendado)."""

            pipe_spawn_counter = 0  # Um contador com o tempo de spawn.

        # CRIAR OBJETOS #######################

        # Botão de Pause
        # rect = self.res['pause_button'].get_rect()
        # rect.center = (30, 30)
        # rectangle = self.res['pause_button'].get_rect().size
        # TODO: Fazer botão de pause

        # Criar objetos principais
        player = Player(INIT_POSITION, self.res["bird"], linked_game=self)

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
                    Tile((0, self.ground_pos), self.res["floor"], factor=1),
                    Tile((1600, self.ground_pos), self.res["floor"], factor=1),
                ],
                # Tiles do Fundo (background)
                [
                    Tile((0, 0), [self.res["bg"]], factor=0.5),
                    Tile((1600, 0), [self.res["bg"]], factor=0.5),
                ],
            )

        floor_tiles, bg_tiles = ([], [])  # Um patch preguiçoso que cria as listas de tiles antes de preenchê-las para poder fazer o código mais abaixo funcionar.

        # LOOP PRINCIPAL (FRAMES) #############

        while running:

            # Variáveis atualizadas no início do frame
            var.pipe_spawn_delay = 200 / self.speed

            # Limitar a quantidade de frames.
            self.clock.tick(FRAMERATE)

            # INPUT & FÍSICA ##################

            # Atualizar as teclas e entradas de mouse pressionadas.
            self.input.process()

            # Atualizar o jogador
            player.process()

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
                        height + image_size(self.res["tube_top"])[1] + spacing
                    )

                    # Criar o cano de cima
                    new_pipe_top = Pipe(
                        (WINSIZE[0], height), self.res["tube_top"], None, self.speed
                    )
                    pipes_list.append(new_pipe_top)

                    # Criar o cano de baixo
                    new_pipe_bottom = Pipe(
                        (WINSIZE[0], bottom_pipe_height),
                        self.res["tube_bottom"],
                        None,
                        self.speed,
                    )
                    pipes_list.append(new_pipe_bottom)

                    # Resetar o counter
                    var.pipe_spawn_counter = var.pipe_spawn_delay

                # Iterar os canos
                for (pipe_index, pipe) in enumerate(pipes_list):

                    pipe.process() # Atualizar os canos
                    pipe_hitbox = gameobject_hitbox(pipe) # Criar hitbox do cano

                    # Morte pela colisão entre jogador e cano
                    if pipe_hitbox.colliderect(gameobject_hitbox(player)):
                        self.state = 2
                        player.speed.y = -8

                    # Pontos ao passar pelo cano
                    # Parte do código está na classe do pipe.
                    if player.pos.x > pipe.pos.x + pipe_hitbox[3]:
                        if not pipe.has_scored:
                            self.score += 1
                            pipe.has_scored = True

                    # Despawnar o cano quando ele sair da esquerda da tela.
                    if pipe.pos.x < (0 - gameobject_size(pipe)[0]):
                        del pipes_list[pipe_index]

            # Iterar logo tudo
            # Colocar isso antes da preparação das listas do primeiro frame para que o jogo não comece com os itens se mexendo já para trás.
            if self.state in {0, 1}:
                for tile_list in (floor_tiles, bg_tiles):
                    for tile in tile_list:
                        # Mexer na velocidade
                        # Parallax para isso pode ser definido pela key 'factor' no atributo 'kwargs' dos objetos iterados aqui.
                        tile.pos.x -= self.speed * tile.kwargs["factor"]
                        # Mover o tile para a direita se ele já saiu completamente da tela.
                        if tile.pos.x < (0 - gameobject_size(tile)[0]):
                            tile.pos.x = WINSIZE[0]

            # Preparar as listas de floor e background no primeiro do jogo.
            # Funciona também com resets - basta definir o valor do timer para 0.
            if self.timer == 0:
                floor_tiles, bg_tiles = make_tiles()
                pipes_list = []
                self.state = 0
                player.angle_target = player.angle = 0
                player.speed.y = 0
                player.pos.x, player.pos.y = INIT_POSITION

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
                screen.blit(self.res["tip"], (80, 0))

            # Mostrar o botão de pause
            # FIXME: Fazer esse botão realmente funcionar. Parece estar errado.
            # screen.blit(self.res['pause_button'], (0, 0)) # tinha um rect no lugar de (0, 0), mas eu não sei pq.

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
                    self.res["game_over"], (100, 0)
                )  # TODO: Cálculo de posicionamento melhor

            # Atualizar a Tela
            pygame.display.update()

            # POST-PROCESSING #################

            # Processamento de eventos
            for event in pygame.event.get():

                # Sair pelo comando sair da janela (Botão X no canto, Alt+F4 etc.)
                if event.type == QUIT:
                    running = False

            # Adicionar 1 ao timer
            self.timer += 1

if (__name__ == "__main__"):
    from sys import argv
    main(argv)
