import pygame
from pygame.locals import *
import random

# Variables
STAY = 0
JUMP = 1
blue = (115, 200, 215)

# Inicia o jogo
pygame.init()

# Prepara a aba
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('Models/Icon.bmp')
pygame.display.set_icon(icon)

# Background Image
background = pygame.image.load('Models/Background.png')
floor = pygame.image.load('Models/Floor.png')

# Bird Jump
isjumpping = False

# Bird
bird_pos = (375, 275)
bird = pygame.image.load('Models/Bird_0.png')

# Tubes
tube_top = pygame.image.load('Models/Tube_Top.png')
tube_bottom = pygame.image.load('Models/Tube_Bottom.png')

clock = pygame.time.Clock()
tick = 10

while True:

    # Limita os Frames
    clock.tick(tick)

    # Sair do Jogo
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # Pular
    if event.type == KEYDOWN:
        if event.key == K_UP:
            isjumpping = True

            print('Jump')

    # Screen
    screen.fill(blue)
    screen.blit(bird, bird_pos)
    screen.blit(background, (0, 0))

    a = random.randint(0, 4)

    x = 400 - (50 * a)
    y = 0 - (50 * a)

    screen.blit(tube_bottom, (700, x))
    screen.blit(tube_top, (700, y))
    screen.blit(floor, (0, 476))

    pygame.display.update()
