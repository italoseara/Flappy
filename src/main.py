import sys
import platform
import os

# Verify python version (3.x+)
major_version = platform.python_version()[0]
if not (major_version == "3"):
    print(f"Major python version needs to be 3 (current is {major_version}).", file=sys.stderr)
    sys.exit(1)

# Import pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Local Modules
import core # utilidades, classes etc.
import game # o jogo em si

# initialize game (whether the file was opened directly)
if __name__ == "__main__":
    pygame.init()
    game.main()
