# vim: foldmethod=marker
# INICIALIZAÇÃO {{{

# Pygame & Stdlib
import pygame
from pygame.locals import *
from random import randint

# Módulos Locais
from lib.game import *
from lib.input import InputHandler, BUTTON_LEFT, BUTTON_MIDDLE, BUTTON_RIGHT
from lib.obj import *
from lib.data import *
from lib.maths import *

pygame.init()

# }}}
# CONFIGURAÇÕES {{{

class cfg:

    # Imagens
    RESOURCES = [
        ("icon", "res/icon.bmp"),
        ("floor", "res/floor.png"),
        ("bg", "res/background.png"),
        ("bird", "res/bird_f0.png"),
        ("pipe_top", "res/pipe_top.png"),
        ("pipe_bot", "res/pipe_bot.png"),
        ("starter_tip", "res/starter_tip.png"),
        ("game_over", "res/game_over.png"),
        ("pause_button", "res/pause.png"),
        ("menu", "res/menu.png"),
    ]

    # Tamanho da janela
    WINSIZE = (960, 540)
    BACKGROUND_COLOR = (115, 200, 215)
    SPEED = 3
    FRAMERATE = 60
    GRAVITY = 0.5
    PARALLAX_BG = 0.5
    PARALLAX_FLOOR = 1.0
    PIPE_HEIGHT_INTERVAL = (-210, -40)
    PIPE_Y_SPACING = 130
    JUMP_SPEED = -8
    HITBOX_COLOR = (255, 0, 0)
    HITBOX_WIDTH = 2
    FONT = pygame.font.SysFont("Ubuntu Mono, Cascadia Code, Consolas, Fixedsys", 20)
    FONT_COLOR = pygame.Color("white")
    FONT_POS = (15, 10)
    FONT_ENABLED = True
    DEBUG = True
    GROUND_POS = 476

# }}}
# FUNÇÕES DE AJUDA {{{

def run_game(fn):
    fn(DataSpace(), cfg)

# }}}
# PARTE PRINCIPAL {{{

def game_function(d, cfg):
    """Código principal do jogo, que coordena todos os objetos."""
    # INICIALIZAÇÃO DE VARIÁVEIS {{{
    d.cfg = cfg
    d.debug_mode = cfg.DEBUG
    d.res = resource_dict(cfg.RESOURCES)
    d.input = InputHandler()
    d.clock = pygame.time.Clock()
    d.timer = state = score = 0

    d.bird_init_position = (
        cfg.WINSIZE[0] / 2 - image_size(d.res["bird"])[0] / 2,
        cfg.WINSIZE[1] / 2 - image_size(d.res["bird"])[1] / 2,
    )

    # Definir a janela
    d.screen = pygame.display.set_mode(cfg.WINSIZE)
    pygame.display.set_caption(
        "({}x{}), Flappy Bird but it's weird".format(*cfg.WINSIZE)
    )
    pygame.display.set_icon(d.res["icon"])

    d.pipe_spawn_counter = 0 # Um contador com o tempo para spawn dos canos.

    # Outras opções
    d.game_state = 0
    d.score = 0
    d.running = True

    # }}}
    # FUNÇÕES {{{

    def make_tiles():
        return (
            # Chão (floors)
            [Tile((x, cfg.GROUND_POS), d.res["floor"], d, cfg.PARALLAX_FLOOR) for x in [0, 1600]],
            # Fundo (bgs)
            [Tile((x, 0), d.res["bg"], d, cfg.PARALLAX_BG) for x in [0, 1600]],
        )

    # }}}
    # CRIAR OBJETOS {{{

    # Botão de Pause
    # rect = d.res['pause_button'].get_rect()
    # rect.center = (30, 30)
    # rectangle = d.res['pause_button'].get_rect().size
    # TODO: Fazer botão de pause

    # Jogador e Cenário
    player = Player(d.bird_init_position, d.res["bird"], d)
    d.floors, d.bgs, d.pipes = [], [], []

    # }}}
    # LOOP PRINCIPAL {{{
    while d.running:
        # INÍCIO DO FRAME {{{

        # Forçar o Framerate
        d.clock.tick(cfg.FRAMERATE)

        # Atualizar algumas variáveis
        d.pipe_spawn_delay = 200 / cfg.SPEED

        # Step Processing
        d.input.process()
        player.process()

        # }}}
        # PROCESSAMENTO & FÍSICA {{{

        if d.game_state == 1:
            d.pipe_spawn_counter -= 1

            for (i, pipe) in enumerate(d.pipes):
                pipe.process()
                pipe_hitbox = gameobject_hitbox(pipe)

                # Pontos ao passar pelo cano
                # Parte do código está na classe do pipe.
                if (not pipe.has_scored) and (player.pos.x > pipe.pos.x + pipe_hitbox[3]):
                    d.score += 1
                    pipe.has_scored = True

                # Morte na colisão entre o jogador e um cano
                if pipe_hitbox.colliderect(gameobject_hitbox(player)):
                    d.game_state = 2
                    player.speed.y = cfg.JUMP_SPEED
                    break

                # Despawnar o cano quando ele sair da esquerda da tela.
                if pipe.pos.x < 0 - gameobject_size(pipe)[0]:
                    del d.pipes[i]
                    print(len(d.pipes))

            # Spawnar dois canos (um em cima e um em baixo) quando o counter acabar.
            if d.pipe_spawn_counter <= 0:
                top_y = randint(*cfg.PIPE_HEIGHT_INTERVAL)
                bot_y = top_y + image_size(d.res["pipe_top"])[1] + cfg.PIPE_Y_SPACING

                top_pipe = Pipe((cfg.WINSIZE[0], top_y), d.res["pipe_top"], d, cfg.SPEED)
                bot_pipe = Pipe((cfg.WINSIZE[0], bot_y), d.res["pipe_bot"], d, cfg.SPEED)

                d.pipes += [top_pipe, bot_pipe]
                d.pipe_spawn_counter = d.pipe_spawn_delay

        # Iterar tiles
        # Colocar isso antes da preparação das listas do primeiro frame para que o jogo não comece com os itens se mexendo já para trás.
        if d.game_state in {0, 1}:
            for tile in (d.floors + d.bgs):
                # Atualizar a posição com base na velocidade
                tile.pos.x -= cfg.SPEED * tile.parallax_coeff
                # Mover o tile para a direita se ele saiu completamente da tela.
                if tile.pos.x < 0 - gameobject_size(tile)[0]:
                    tile.pos.x = cfg.WINSIZE[0]

        # Preparar as listas de floor e background no primeiro frame do jogo.
        # Isto é utilizado também com resets.
        if d.timer == 0:
            d.pipes.clear()
            d.floors, d.bgs = make_tiles()
            d.game_state = 0

            player.angle_target = player.angle = 0
            player.speed.y = 0
            player.pos.x, player.pos.y = d.bird_init_position

        # }}}
        # INPUT {{{

        # Toggle hitboxes
        if d.input.keymap[K_h].first:
            d.debug_mode = not d.debug_mode

        # }}}
        # RENDERIZAÇÃO {{{

        # Fundo (céu)
        d.screen.fill(cfg.BACKGROUND_COLOR)

        # Renderizar background e canos
        for obj in d.bgs + d.pipes:
            gameobject_render(obj, d.screen)

        # Renderizar jogador
        gameobject_render(player, d.screen)

        # Renderizar hitboxes dos canos
        if d.debug_mode:
            for pipe in d.pipes:
                pygame.draw.rect(d.screen, cfg.HITBOX_COLOR, gameobject_hitbox(pipe), cfg.HITBOX_WIDTH)

        # Renderizar chão
        for obj in d.floors:
            gameobject_render(obj, d.screen)

        # Renderizar hitbox do chão
        if d.debug_mode:
            pygame.draw.rect(d.screen, cfg.HITBOX_COLOR, (0, cfg.GROUND_POS, *cfg.WINSIZE), cfg.HITBOX_WIDTH)

        # Mostrar a dica inicial
        # TODO: Fazer um posicionamento melhor (cálculos de centralização, talvez rect.center)
        if d.game_state == 0:
            d.screen.blit(d.res["starter_tip"], (80, 0))

        # Mostrar o botão de pause
        # FIXME: Fazer esse botão realmente funcionar. Parece estar errado.
        # screen.blit(d.res['pause_button'], (0, 0)) # tinha um rect no lugar de (0, 0), mas eu não sei pq.

        # Texto no topo da tela
        if cfg.FONT_ENABLED:
            debug_text = "{debug_flag}Score: {score}; FPS: {fps}".format(
                    debug_flag="[DEBUG] " if d.debug_mode else "",
                    score=d.score,
                    fps=int(d.clock.get_fps()),
            )
            fps_text = cfg.FONT.render(debug_text, True, cfg.FONT_COLOR)
            d.screen.blit(fps_text, cfg.FONT_POS)

        if d.game_state == 2:
            d.screen.blit(d.res["game_over"], (100, 0)) # TODO: Fazer cálculo de posicionamento melhor

        # Atualizar a tela
        pygame.display.update()

        # }}}
        # POST-PROCESSING {{{

        # Processamento de eventos
        for event in pygame.event.get():

            # Sair pelo comando sair da janela (Botão X no canto, Alt+F4 etc.)
            if event.type == QUIT:
                d.running = False

        # Adicionar 1 ao timer
        d.timer += 1

        # }}}

# }}}

# INICIALIZAÇÃO DO JOGO {{{

if __name__ == "__main__":
    run_game(game_function)

# }}}
