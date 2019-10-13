import pygame
from pygame.locals import *
import random

STAY = 0
JUMP = 1

blue = (115, 200, 215)

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('Models//Icon.bmp')
pygame.display.set_icon(icon)

background = pygame.image.load('Models//Background.png')

my_direction = STAY

bird_pos = (375, 275)
bird = [pygame.image.load('Models//Bird_0.png'),
        pygame.image.load('Models//Bird_1.png'),
        pygame.image.load('Models//Bird_2.png')]

frame_bird = 0
verify = False

clock = pygame.time.Clock()
tick = 10

while True:
    clock.tick(tick)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    if verify:

        if frame_bird == 2:
            verify = False
            frame_bird = 0

        screen.blit(bird[frame_bird], bird_pos)

        frame_bird += 1

    if event.type == KEYDOWN:
        if event.key == K_UP:
            my_direction = JUMP

            verify = True

            print('Jump')

    else:
        screen.blit(bird[0], bird_pos)

    screen.fill(blue)
    screen.blit(background, (0, 0))

    pygame.display.update()
