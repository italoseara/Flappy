import pygame
from pygame.locals import *
import random

# Cores
blue = (115, 200, 215)

# Inicia o Pygame
pygame.init()


# Carregar as imagens
class Img:
    # Atalho kj
    load = pygame.image.load

    # Imagens mesmo
    icon = load('Models/Icon.bmp')
    floor = load('Models/Floor.png')
    bg = load('Models/Background.png')
    bird = [load('Models/Bird_0.png'),
            load('Models/Bird_1.png'),
            load('Models/Bird_2.png')]
    tube_top = load('Models/Tube_Top.png')
    tube_bottom = load('Models/Tube_Bottom.png')
    tip = load('Models/Init.png')


# Título e ícone
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(Img.icon)

# Iniciar variáveis
isJumping = False  # "Está pulando?"


class Bird:
    pos = [375, 275]  # Posição
    animFrame = 0  # Frame da animação
    yspeed = 0  # Velocidade Y


# Classe de Input
class Input:
    # Pressed Keys: verdadeiro só no primeiro frame em que a tecla é pressionada.
    # É bom para ações como pular, em que você aperta o botão uma vez e se segurar nãofaz diferença.
    keyUpPressed = False  # Para cima

    # (Held) Keys: verdadeiro em qualquer momento que a tecla for pressionada.
    keyUp = False  # Para cima


# Outros componentes do jogo
clock = pygame.time.Clock()
tick = 60
timer = 0

running = True
while running:

    # Limitar a quantidade de frames
    clock.tick(tick)

    # Input etc.
    _keyMap = pygame.key.get_pressed()
    if _keyMap[pygame.K_UP]:
        if Input.keyUp:
            Input.keyUpPressed = False
        else:
            Input.keyUpPressed = True
    Input.keyUp = _keyMap[pygame.K_UP]

    #################
    # CD. PRINCIPAL #
    #################

    # Iniciar o pulo
    if not isJumping:
        if Input.keyUpPressed:
            isJumping = True
            Bird.yspeed = -8
            print('(A) Jumped', timer)

    # Iterar a gravidade
    Bird.pos[1] += Bird.yspeed
    Bird.yspeed += 0.5

    # (E|I)ntalar no chão ou no céu
    Bird.pos[1] = max(0, min(Bird.pos[1], 476 - 30))

    # Morrer
    # if Bird.pos[1] == 476-30: running = False

    ##########
    # POLISH #
    ##########

    # Colocar o fundo
    screen.fill(blue)
    screen.blit(Img.bg, (0, 0))

    # Colocar o pássaro
    if isJumping:
        Bird.animFrame += 1
        if Bird.animFrame >= 2:
            isJumping = False
            Bird.animFrame = 0
    screen.blit(Img.bird[Bird.animFrame], Bird.pos)

    # Colocar os tubos na tela
    a = random.randint(0, 4)
    x = 400 - 50 * a
    y = 0 - 50 * a

    screen.blit(Img.tube_bottom, (700, 400))
    screen.blit(Img.tube_top, (700, 0))

    # Colocar o chão
    screen.blit(Img.floor, (0, 476))

    # Colocar dica inicial
    if timer < 200:
        screen.blit(Img.tip, (0, 0))

    # Atualizar a tela
    pygame.display.update()

    ###################
    # POST-PROCESSING #
    ###################

    # Processamento de eventos
    for event in pygame.event.get():

        if event.type == QUIT:
            running = False

    # Adicionar 1 ao timer
    timer += 1
