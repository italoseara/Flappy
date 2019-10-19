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
            load('img/bird_f2.png')],
    'tube_top': load('img/tube_top.png'),
    'tube_bottom': load('img/tube_bottom.png'),
    'tip': load('img/tip.png')
}

# Título, ícone, e outras coisas
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(img['icon'])

# Startup screen
screen.fill((0, 0, 0))
screen.blit(
        pygame.font.Font(None, 50).render('Loading...', True, pygame.Color('white')),
        (400, 300)
)

# Load fonts
font = pygame.font.SysFont('Consolas', 50)

# Outras coisas
COLOR_BLUE = (115, 200, 215) # A cor de fundo do jogo.
FRAMERATE = 60 # O framerate do jogo.
gameTimer = 0 # O timer do jogo.
clock = pygame.time.Clock()
gameSpeed = [-1]

# Importar objetos e outras coisas
import objects, inputlib, log, random
pipes = list()
player = objects.Bird([375, 275], img['bird'], groundPointY=476)
pinput = inputlib.PlayerInput()
log = log.Log(enabled=True)
floorTiles = [objects.RepeatingTile((0, 476), [img['floor']], gameSpeed)]
bgTiles = [objects.RepeatingTile((0, 0), [img['bg']], [gameSpeed[0]/2])]

# Canos (pipes)
base_pipeSpawnDelay = 210
pipeSpawnDelay = 0

# Início do jogo
running = True

while running:

    # Limitar a quantidade de frames.
    clock.tick(FRAMERATE)

    # Atualizar as teclas pressionadas.
    pinput.iterate()

    # CÓDIGO PRINCIPAL ###################################################
    
    player.manage()
    # Sistema de pulo
    if (not player.isJumping):
        # PROBLEMA - o pulo não está indo direito.
        if (pinput.keyUp[1]):
            player.isJumping = True
            player.ySpeed = -8
            #log.print('[{}] Jumped'.format(gameTimer))

    # Um tempo (em frames) para que fique um espaço livre entre os canos.
    pipeSpawnDelay -= 1

    # Sempre encher a lista de canos
    if (pipeSpawnDelay <= 0):

        height = random.randint(-190, 0)
        topTubeHeight = img['tube_top'].get_rect().size[1]

        # Canos topo e baixo
        pipes.append(objects.Pipe((800, height), [img['tube_top']], gameSpeed))
        pipes.append(objects.Pipe((800, height+topTubeHeight+155), [img['tube_bottom']], gameSpeed))

        pipeSpawnDelay = base_pipeSpawnDelay

    # Sempre encher as listas de floor e background

    if (len(floorTiles) < 2):
        floorTiles.append(objects.RepeatingTile((1600, 476), [img['floor']], gameSpeed))
    for floor in floorTiles:
        floor.manage()
        if floor.pos[0] < 0-floor.frames[0].get_rect().size[0]:
            floorTiles.remove(floor)
            del floor

    if (len(bgTiles) < 2):
        bgTiles.append(objects.RepeatingTile((800, 0), [img['bg']], [gameSpeed[0]/2]))
    for bg in bgTiles:
        bg.manage()
        if bg.pos[0] < 0-bg.frames[0].get_rect().size[0]:
            bgTiles.remove(bg)
            del bg

    # Atualizar os canos
    for pipe in pipes:
        pipe.manage()
        if pygame.Rect(*pipe.hitbox()).colliderect(pygame.Rect(*player.hitbox())):
            
            running = False
        if pipe.pos[0] < 0-pipe.frames[0].get_rect().size[0]:
            pipes.remove(pipe)
            del pipe

    # (Teste) aceleração dos canos
    #gameSpeed[0] += -0.05

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
    for pipe in pipes:
        pygame.draw.rect(screen, (255, 0, 0), pipe.hitbox(), 2)
    pygame.draw.rect(screen, (0, 255, 0), player.hitbox(), 2)

    # Chão
    for floor in floorTiles:
        screen.blit(*floor.render())
    if player.isDead: running = False

    # FPS
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    screen.blit(fps, (790-fps.get_rect().size[0], 10))

    # Atualizar a Tela
    pygame.display.update()

    # POST-PROCESSING ####################################################

    # Processamento de eventos
    for event in pygame.event.get():

        if event.type == QUIT:
            running = False

    # Adicionar 1 ao timer
    gameTimer += 1
