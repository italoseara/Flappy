# Imports iniciais
import pygame
from pygame.locals import *
import random

# Variáveis 
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
rotate = 0
clock = pygame.time.Clock()
FPS = 60
timer = tube1 = tube2 = tube3 = tube4 = 0
colliding = []
a = [random.randint(0, 210), random.randint(0, 210), random.randint(0, 210), random.randint(0, 210)]
x = [430 - a[0], 430 - a[1], 430 - a[2], 430 - a[3]]
y = [0 - a[0], 0 - a[1], 0 - a[2], 0 - a[3]]

running = True
start = True

while running:

    if start:
        # Limitar a quantidade de frames
        clock.tick(FPS)

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

        # Rotacionar imagem

        # Iterar a gravidade
        Bird.pos[1] += Bird.yspeed
        Bird.yspeed += 0.5

        # Intalar no chão ou no céu
        if Bird.pos[1] < 0:
            Bird.pos[1] = 0
            Bird.yspeed = 0
        elif Bird.pos[1] >= 476-30: 
            Bird.pos[1] = 476-30
            Bird.yspeed = 0
            # running = False # Morrer

        # POLINDO ###################################################################

        # Colocar o fundo
        screen.fill(blue)
        screen.blit(Img.bg, (0, 0))

        #############################################################################

        # Coloca os tubos na tela

        if timer >= 0:
            tube1 += 1

            screen.blit(Img.tube_bottom, (800 - tube1, x[0]))
            screen.blit(Img.tube_top, (800 - tube1, y[0]))

            # HitBox
            tube1_bottom = Img.tube_bottom.get_rect()
            tube1_bottom.center = (800 - tube1 + 34, x[0] + 155)
            tube1_top = Img.tube_top.get_rect()
            tube1_top.center = (800 - tube1 + 34, y[0] + 155)

            # Desenha a hitbox
            pygame.draw.rect(screen, (255, 0, 0), tube1_bottom, 2)
            pygame.draw.rect(screen, (255, 0, 0), tube1_top, 2)

        if tube1 == 860:
            tube1 = 0

            a[0] = random.randint(0, 210)

        if timer >= 210:
            tube2 += 1

            screen.blit(Img.tube_bottom, (800 - tube2, x[1]))
            screen.blit(Img.tube_top, (800 - tube2, y[1]))

            # Hitbox
            tube2_bottom = Img.tube_bottom.get_rect()
            tube2_bottom.center = (800 - tube2 + 34, x[1] + 155)
            tube2_top = Img.tube_top.get_rect()
            tube2_top.center = (800 - tube2 + 34, y[1] + 155)

            # Desenha a Hitbox
            pygame.draw.rect(screen, (255, 0, 0), tube2_bottom, 2)
            pygame.draw.rect(screen, (255, 0, 0), tube2_top, 2)

        if tube2 == 860:
            tube2 = 0

            a[1] = random.randint(0, 210)

        if timer >= 420:
            tube3 += 1

            screen.blit(Img.tube_bottom, (800 - tube3, x[2]))
            screen.blit(Img.tube_top, (800 - tube3, y[2]))

            # HitBox
            tube3_bottom = Img.tube_bottom.get_rect()
            tube3_bottom.center = (800 - tube3 + 34, x[2] + 155)
            tube3_top = Img.tube_top.get_rect()
            tube3_top.center = (800 - tube3 + 34, y[2] + 155)

            # Desenha a Hitbox
            pygame.draw.rect(screen, (255, 0, 0), tube3_bottom, 2)
            pygame.draw.rect(screen, (255, 0, 0), tube3_top, 2)

        if tube3 == 860:
            tube3 = 0

            a[2] = random.randint(0, 210)

        if timer >= 630:
            tube4 += 1

            screen.blit(Img.tube_bottom, (800 - tube4, x[3]))
            screen.blit(Img.tube_top, (800 - tube4, y[3]))

            # HitBox
            tube4_bottom = Img.tube_bottom.get_rect()
            tube4_bottom.center = (800 - tube4 + 34, x[3] + 155)
            tube4_top = Img.tube_top.get_rect()
            tube4_top.center = (800 - tube4 + 34, y[3] + 155)

            # Desenha a Hitbox
            pygame.draw.rect(screen, (255, 0, 0), tube4_bottom, 2)
            pygame.draw.rect(screen, (255, 0, 0), tube4_top, 2)

        if tube4 == 860:
            tube4 = 0

            a[3] = random.randint(0, 210)

        #############################################################################

        # Colocar o chão
        screen.blit(Img.floor, (0, 476))

        # Colocar o pássaro
        if isJumping:
            Bird.animFrame += 1
            if Bird.animFrame >= 2:
                isJumping = False
                Bird.animFrame = 0

        rotate = Bird.yspeed * -5
        rotate = min(max(rotate, -45), 45)
        rotate = (rotate + 360) % 360

        # Gira o pássaro
        old_center = (Bird.pos[0] + 15, Bird.pos[1] + 15)
        new_img = pygame.transform.rotate(Img.bird[Bird.animFrame], rotate)
        rect = new_img.get_rect()
        rect.center = old_center
        screen.blit(new_img, rect)

        # Desenha a hitbox do pássaro
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)

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
