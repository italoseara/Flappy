#!/usr/bin/env python3
# Clone de Flappy Bird
# Autores: ItaloDoArbusto, YohananDiamond
# Repositório: https://github.com/ItaloDoArbusto/Flappy

# Comentários com "+tag" são anotações com categorização. Alguns dos significados:
# "altousocpu" => Provavelmente utiliza muita CPU ou Memória e pode estar deixando o jogo lento.

# CONSTANTES #####################################
# Esta seção foi feita para colocar constantes que serão utlizadas no andamento do jogo, como tamanho da tela.
# Deixar elas no mesmo lugar faz com que seja mais fácil alterá-las depois.
# Inspirado no '#define' da linguagem C .-.

WINSIZE = (960, 540)        # Tamanho da Tela
FRAMERATE = 60              # O framerate do jogo (fps)

# INICIALIZAÇÃO GERAL ############################

# Importar o pygame e iniciá-lo
import pygame
from pygame.locals import *
pygame.init()

# PARTE PRINCIPAL ##################################

class Game:

    '''Contém o jogo em si.
    As funções principais todas estão localizadas aqui para facilitar a manutenção.'''

    def __init__(self, globalSpeed=1, debugMode=False):

        '''Inicia alguns valores da classe.
        globalSpeed : int -- A velocidade do jogo.'''

        self.timer = 0
        self.clock = pygame.time.Clock()
        self.globalSpeed = globalSpeed
        self.debugMode = debugMode
        self.score = 0

        self.load_resources()

    def load_resources(self):

        '''Carrega os recursos do jogo.'''

        # Arquivos gráficos
        load = pygame.image.load
        self.img = {
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
            'game_over': load('img/game_over.png')
        }

        # Fontes utilizadas
        self.font = pygame.font.SysFont('Cascadia Code, Consolas, Fixedsys', 20) # A fonte principal utilizada no jogo.

    def main(self):

        '''O código do jogo propriamente dito.'''

        # Importar módulos locais
        from objects import Player, Pipe, Tile
        from tools import imgsize, objsize, gethitbox, Logger
        from inputlib import PlayerInput

        # Importar módulos builtins
        from random import randint

        # Definir a janela
        screen = pygame.display.set_mode(WINSIZE)   # Criar Janela
        pygame.display.set_caption('Flappy Bird')   # Definir Título
        pygame.display.set_icon(self.img['icon'])        # Definir Ícone

        # Constantes locais ao jogo
        COLOR_BACKGROUND = (115, 200, 215)  # RGB do fundo
        INIT_POSITION = (WINSIZE[0]/2 - imgsize(self.img['bird'][0])[0]/2, WINSIZE[1]/2 - imgsize(self.img['bird'][0])[1]/2)          # Posição inicial do jogo

        class var:

            '''Uma subclasse que contém algumas variáveis para o jogo.
            Elas estão aqui porque estão relacionadas a algum objeto ou não são constantes.
            Isso pode ser utilizado também quando se quer criar uma variável que funcione em todos os frames, mas quando está dentro do loop principal (não tão recomendado).'''

            pipeSpawnCounter = 0 # Um contador com o tempo de spawn.

        # INICIALIZAÇÃO DA FASE ##########################

        # Criar objetos principais
        player = Player(pos = list(INIT_POSITION), frames = self.img['bird'], deathHeightBottom = 476)
        pinput = PlayerInput()
        logger = Logger(enabled = self.debugMode)

        # Criar objetos do cenário (canos, fundo, chão etc.)
        floorTiles, pipes, bgTiles = [], [], []

        # Variáveis para o início do jogo
        running = True
        gameState = 0 # 0 para 'inicial (introdução)', 1 para 'jogo iniciado', 2 para 'morte'

        # FUNÇÕES ################################################

        def makeTiles():
            '''Faz os tiles quando o jogo inicia (gameState == 1) ou quando ele é resetado.'''
            floorTiles = [
                Tile((0,476), [self.img['floor']], factor=1),
                Tile((1600,476), [self.img['floor']], factor=1)]
            bgTiles = [
                Tile((0,0), [self.img['bg']], factor=0.5),
                Tile((1600,0), [self.img['bg']], factor=0.5)]
            return floorTiles, bgTiles

        # INÍCIO DO LOOP PRINCIPAL (FRAMES) ######################

        while running:

            # Variáveis atualizadas no início do frame
            var.pipeSpawnDelay = 200 / self.globalSpeed
            # Limitar a quantidade de frames.
            self.clock.tick(FRAMERATE)

            # INPUT E FÍSICA ###################################################

            # Atualizar as teclas pressionadas.
            pinput.iterate()

            # Pular
            if (pinput.keyUp[1]):

                # Iniciar o jogo
                if (gameState == 0):
                    gameState = 1

                if (gameState != 2):
                    player.isJumping = True
                    player.ySpeed = -8

            # Atualizar o jogador e enviar a ele algumas variáveis que estão sendo utilizadas.
            player.manage(gameState=gameState)

            if (gameState == 1): # "Jogo Iniciado"

                # Diminuir do contador de spawn de canos.
                var.pipeSpawnCounter -= 1

                # Spawnar alguns canos de vez em quando.
                if (var.pipeSpawnCounter <= 0):

                    # Achar valor aleatório para o spawn do cano.
                    height = randint(-210, -40)
                    spacing = 130
                    bottomPipeHeight = height + imgsize(self.img['tube_top'])[1] + spacing

                    # Criar o cano de cima
                    newPipeTop = Pipe((WINSIZE[0], height), [self.img['tube_top']], self.globalSpeed)
                    pipes.append(newPipeTop)

                    # Criar o cano de baixo
                    newPipeBottom = Pipe((WINSIZE[0], bottomPipeHeight), [self.img['tube_bottom']], self.globalSpeed)
                    pipes.append(newPipeBottom)

                    # Resetar o counter
                    var.pipeSpawnCounter = var.pipeSpawnDelay

                # Iterar os canos (+altousocpu)
                for pipeID, pipe in enumerate(pipes):

                    # Atualizar os canos
                    pipe.manage()

                    # Colisão entre jogador e cano
                    if gethitbox(pipe).colliderect(gethitbox(player)):
                        player.isDead = True

                    if player.pos[1] == pipe.pos[1]:
                        self.score += 1

                    # Despawnar o cano quando ele sair da esquerda da tela.
                    if pipe.pos[0] < (0 - objsize(pipe)[0]):
                        del pipes[pipeID]

            # Iterar logo tudo.
            # Colocar isso antes da preparação do primeiro frame para que o jogo não comece com os itens se mexendo já para trás.
            if (gameState <= 1):
                for ls in (floorTiles, bgTiles):
                    for item in ls:

                        # Mexer na velocidade (com direito a parallax, via a entrada 'factor' em kwargs.)
                        item.pos[0] -= self.globalSpeed * item.kwargs['factor']

                        # Mover o tile na direita se ele já saiu completamente da tela.
                        if item.pos[0] < (0 - objsize(item)[0]):
                            item.pos[0] = WINSIZE[0]

            # Preparar as listas de floor e background no primeiro frame
            if (self.timer == 0):
                floorTiles, bgTiles = makeTiles()

            # Verificar se uma tecla foi pressionada após o jogador ter morrido para que o jogo reinicie..
            # Isso deve ser colocado antes do código abaixo para não ocorrer de o jogo fechar no mesmo frame em que o jogador morrer porque ele tinha apertado a tecla.
            if (gameState == 2 and pinput.keyUp[1]):
                floorTiles, bgTiles = makeTiles()
                pipes = []
                gameState = 0
                player.isDead = False
                player.isJumping = True # Tive que forçar oof
                player.pos = list(INIT_POSITION)

            # Congelar o jogo se o jogador tiver morrido
            if player.isDead: gameState = 2

            # RENDERIZAÇÃO #######################################################

            screen.fill(COLOR_BACKGROUND) # Preencher o fundo (céu)

            for bg in bgTiles: screen.blit(*bg.render())            # Background
            for pipe in pipes: screen.blit(*pipe.render())          # Canos
            for floor in floorTiles: screen.blit(*floor.render())   # Chão
            screen.blit(*player.render(gameState))                  # Jogador

            if gameState == 0:
                screen.blit(self.img['tip'], (80, 0))

            # Hitboxes
            if (self.debugMode):
                drect = pygame.draw.rect
                for pipe in pipes: drect(screen, (255, 0, 0), gethitbox(pipe), 2)
                drect(screen, (0, 255, 0), gethitbox(player), 2)

            # FPS
            debug_text = 'Score: {} | FPS: {}'.format(self.score, int(self.clock.get_fps()))
            padding = (10, 10)
            fps = self.font.render(debug_text, True, pygame.Color('white'))
            screen.blit(fps, (padding[0], padding[1]))

            # Tela de Game Over
            if (gameState == 2): screen.blit(self.img['game_over'], (100, 0))

            # Atualizar a Tela
            pygame.display.update()

            # POST-PROCESSING ####################################################

            # Processamento de eventos
            for event in pygame.event.get():

                # Sair pelo comando "sair" na janela (botão X, Alt+F4 etc.)
                if event.type == QUIT:
                    running = False

            # Adicionar 1 ao timer
            self.timer += 1

# Rodar o jogo diretamente se não importado.
if (__name__ == '__main__'):

    #from sys import argv # Para argumentos, vou utilizar depois.

    game = Game(3, False)       # Cria uma instância do jogo.
    game.main()         # Inicia o jogo
