import pygame
from pygame.locals import *

'''Uma série de objetos utilizados no jogo.'''

class GameObject:

    '''Uma base para as outras classes do jogo, como o jogador.'''

    def __init__(self): ...

class Player(GameObject):

    '''Classe com atributos do jogador (pássaro).'''

    def __init__(self, pos, frames, gravity=0.5, deathHeightBottom=476):

        self.pos = list(pos)
        self.animFrame = 0
        self.ySpeed = 0
        self.isJumping = False
        self.frames = list(frames)
        self.angle = 0
        self.colliding = list()
        self.gravity = gravity
        self.hitboxSize = self.frames[0].get_rect().size
        self.deathHeightBottom = deathHeightBottom
        self.isDead = False
        self.angle = 0
        self.jumpCounter = 0
        self.rotateTarget = 0

    def manage(self, gameState):

        '''Uma função que automaticamente roda as funções que são verificadas a cada frame.'''
        if (gameState == 1): self.movement()

    def render(self, gameState, timer2):

        if (gameState == 1):
            self.jumpCounter += 1

        if timer2 == 8:
            self.animFrame += 1

        if self.animFrame >= 4:
            self.isJumping = False
            self.animFrame = 0
        self.jumpCounter = 0

        if self.isDead:
            self.rotateTarget = self.angle = 0
            self.animFrame = 3

        elif (not self.isDead and (gameState == 1)):

            # Achar ângulo
            if self.isJumping: self.rotateTarget = 30
            if self.jumpCounter >= 30: self.rotateTarget = -60

            # Girar o pássaro
            self.angle += (self.rotateTarget - self.angle) * 0.15

            self.rotateTarget = (self.rotateTarget + 360) % 360


        # Atualizar o ang. do pássaro
        old_center = (self.pos[0] + 15, self.pos[1] + 15)
        new_img = pygame.transform.rotate(self.frames[self.animFrame], self.angle)
        rect = new_img.get_rect()
        rect.center = old_center

        return (new_img, rect)

    def movement(self):

        '''Executa as rotinas de movimento de (supostamente) cada frame.'''

        self.pos[1] += self.ySpeed
        self.ySpeed += self.gravity

        if self.pos[1] < 0:
            self.pos[1] = 0
            self.ySpeed = 0
        elif self.pos[1] >= ((self.deathHeightBottom) - self.hitboxSize[1]):
            self.pos[1] = ((self.deathHeightBottom) - self.hitboxSize[1])
            self.ySpeed = 0
            self.isDead = True

    def hitbox(self):

        rect = self.frames[0].get_rect().size
        return tuple(self.pos) + rect

class Pipe(GameObject):

    '''Código relacionado ao cano.'''

    def __init__(self, pos, frames, speed=1):
        self.pos = list(pos)
        self.frames = list(frames)
        self.hitboxSize = self.frames[0].get_rect().size
        #if len(speed) != 1: raise ValueError('The speed list should only contain one element.') # Old check for when it was a list.
        self.speed = speed

    def manage(self):

        # Atualizar a posição
        self.pos[0] += -1 * self.speed

    def hitbox(self):

        rect = self.frames[0].get_rect().size
        return tuple(self.pos) + rect

    def render(self):
        return (self.frames[0], self.pos)

class Tile(GameObject):

    def __init__(self, pos, frames, speed=1, **kwargs):
        self.pos = list(pos)
        self.frames = list(frames)
        self.speed = speed
        self.kwargs = kwargs # Dados extras

    def render(self):
        return self.frames[0], self.pos
