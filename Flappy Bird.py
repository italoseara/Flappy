import pygame
from pygame.locals import *
import random

# Cores
blue = (115, 200, 215)

# Inicia o Pygame
pygame.init()

# Carregar as imagens
class img:

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

# Título e ícone
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(img.icon)

# Iniciar variáveis
isJumping = False # "Está pulando?"
class bird:
	pos = (375, 275) # Posição
	animFrame = 0 # Frame da animação

# Classe de Input
class Input:

	# Pressed Keys: verdadeiro só no primeiro frame em que a tecla é pressionada. É bom para ações como pular, em que você aperta o botão uma vez e se segurar nãofaz diferença.
	keyUpPressed = False # Para cima

	# (Held) Keys: verdadeiro em qualquer momento que a tecla for pressionada.
	keyUp = False # Para cima

# Outros componentes do jogo
clock = pygame.time.Clock(); tick = 60
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
			print('(A) Jumped', timer)

	##########
	# POLISH #
	##########

	# Colocar o fundo
	screen.fill(blue)
	screen.blit(img.bg, (0, 0))

	# Colocar o pássaro
	if isJumping:
		bird.animFrame += 1
		if bird.animFrame >= 2:
			isJumping = False
			bird.animFrame = 0
	screen.blit(img.bird[bird.animFrame], bird.pos)

	# Colocar os tubos na tela
	a = random.randint(0, 4)
	x = 400 - 50 * a
	y = 0 - 50 * a
	screen.blit(img.tube_bottom, (700, x))
	screen.blit(img.tube_top, (700, y))

	# Colocar o chão
	screen.blit(img.floor, (0, 476))

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

