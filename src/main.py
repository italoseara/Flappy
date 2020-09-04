import sys
import platform
import os

# Verificar se a versão é 3.x
major_version = platform.python_version()[0]
if not (major_version == "3"):
    print(f"Major python version needs to be 3 (current is {major_version}).", file=sys.stderr)
    sys.exit(1)

# Importar pygame (possivelmente sem a mensagem irritante de versão)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Módulos locais
import core # utilidades, classes etc.
import game # o jogo em si

# Iniciar o jogo (se o arquivo foi aberto diretamente)
if __name__ == "__main__":
    pygame.init()
    game.main()
