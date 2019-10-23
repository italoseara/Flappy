# Importar o pygame e iniciá-lo
import pygame
from pygame.locals import *
pygame.init()

# Carregar imagens
load = pygame.image.load
img = {
    'icon': load('img/icon.bmp'),
    'floor': load('img/floor.png'),
    'bg': load('img/background.png'),
    'bird': [load('img/bird_f0.png'),
             load('img/bird_f1.png'),
             load('img/bird_f2.png'),
             load('img/bird_fDead.png')],
    'tube_top': load('img/tube_top.png'),
    'tube_bottom': load('img/tube_bottom.png'),
    'tip': load('img/tip.png'),
    'game_over': load('img/game_over.png'),
    'pause_button': load('img/pause.png')
}

# Título, ícone, e outras coisas
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(img['icon'])

# Load fonts
font = pygame.font.SysFont('Consolas', 50)

# Outras coisas
COLOR_BLUE = (115, 200, 215)  # A cor de fundo do jogo.
FRAMERATE = 60  # O framerate do jogo.
gameTimer = 0  # O timer do jogo.
clock = pygame.time.Clock()
gameSpeed = [-2]

# Importar objetos e outras coisas
import objects, inputlib, log, random
pipes = list()
player = objects.Bird([375, 275], img['bird'], groundPointY=476)
pinput = inputlib.PlayerInput()
log = log.Log(enabled=True)
floorTiles = [objects.RepeatingTile((0, 476), [img['floor']], gameSpeed)]
bgTiles = [objects.RepeatingTile((0, 0), [img['bg']], [gameSpeed[0]/2])]

# Pause
rect = img['pause_button'].get_rect()
rect.center = (30, 30)
rectangle = img['pause_button'].get_rect().size
clicks = 0

# Canos (pipes)
base_pipeSpawnDelay = abs(90*1/gameSpeed[0])
pipeSpawnDelay = 0

# Início do jogo
running = True
tip = True
started = False
frozen = False

while running:

    # Limitar a quantidade de frames.
    clock.tick(FRAMERATE)

    # Atualizar as teclas pressionadas.
    pinput.iterate()

    # CÓDIGO PRINCIPAL ###################################################

    # Mouse
    mouse = pygame.Rect(0, 0, 0, 0)
    mouse.center = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Atualizar o jogador
    player.manage()

    # Sistema de pulo
    if pinput.keyUp[1]:
        tip = False
        player.isJumping = True
        player.ySpeed = -8
        started = player.activated = True

    if started:
        # Um tempo (em frames) para que fique um espaço livre entre os canos.
        pipeSpawnDelay -= 1

        # Sempre encher a lista de canos
        if pipeSpawnDelay <= 0:

            height = random.randint(-210, -40)
            topTubeHeight = img['tube_top'].get_rect().size[1]

            # Canos topo e baixo
            pipes.append(objects.Pipe((800, height), [img['tube_top']], gameSpeed))
            pipes.append(objects.Pipe((800, height+topTubeHeight+130), [img['tube_bottom']], gameSpeed))

            pipeSpawnDelay = base_pipeSpawnDelay

    if not frozen:
        # Sempre encher as listas de floor e background

        if len(floorTiles) < 2:
            floorTiles.append(objects.RepeatingTile((1600, 476), [img['floor']], gameSpeed))
        for floor in floorTiles:
            floor.manage()
            if floor.pos[0] < 0-floor.frames[0].get_rect().size[0]:
                floorTiles.remove(floor)
                del floor

        if len(bgTiles) < 2:
            bgTiles.append(objects.RepeatingTile((800, 0), [img['bg']], [gameSpeed[0]/2]))
        for bg in bgTiles:
            bg.manage()
            if bg.pos[0] < 0-bg.frames[0].get_rect().size[0]:
                bgTiles.remove(bg)
                del bg

    # Atualizar os canos
    if started and (not frozen):
        for pipe in pipes:
            pipe.manage()
            if pygame.Rect(*pipe.hitbox()).colliderect(pygame.Rect(*player.hitbox())):
                player.isDead = True
            if pipe.pos[0] < 0-pipe.frames[0].get_rect().size[0]:
                pipes.remove(pipe)
                del pipe

    # Congelar o jogo se o jogador tiver morrido
    if player.isDead: frozen = True

    # Verificar se uma tecla foi pressionada após o jogador ter morrido.
    if player.isDead and pinput.keyUp[1]: running = False

    # RENDERIZAÇÃO #######################################################

    # Fundo
    screen.fill(COLOR_BLUE)

    # Background
    for bg in bgTiles:
        screen.blit(*bg.render())

    # Canos
    for pipe in pipes:
        screen.blit(*pipe.render())

    # Jogador
    screen.blit(*player.render())

    # Hitboxes
    # for pipe in pipes:
    #     pygame.draw.rect(screen, (255, 0, 0), pipe.hitbox(), 2)
    # pygame.draw.rect(screen, (0, 255, 0), player.hitbox(), 2)
    # pygame.draw.rect(screen, (0, 255, 0), (11, 11) + rectangle, 2)

    # Chão
    for floor in floorTiles:
        screen.blit(*floor.render())

    # Botao de pause
    screen.blit(img['pause_button'], rect)

    # if click[0] == 1 and mouse.colliderect(pygame.Rect((11, 11) + rectangle)):
        # pause = True

    # FPS
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    screen.blit(fps, (790-fps.get_rect().size[0], 10))

    # Tela de Fim de jogo
    if player.isDead: screen.blit(img['game_over'], (0, 0))

    # Dica Inicial
    if tip: screen.blit(img['tip'], (0, 0))

    # Atualizar a Tela
    pygame.display.update()

    # POST-PROCESSING ####################################################

    # Processamento de eventos
    for event in pygame.event.get():

        if event.type == QUIT:
            running = False

    # Adicionar 1 ao timer
    gameTimer += 1
