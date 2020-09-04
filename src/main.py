import sys
import platform
import os

# check if python version is 3.x (needed)
major_version = platform.python_version()[0]
if not (major_version == "3"):
    print(f"Major python version needs to be 3 (current is {major_version}).", file=sys.stderr)
    sys.exit(1)

# import pygame and try to supress the annoying startup message.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# local modules
import core # utilities, classes etc.
import game # the actual game

# start the game (if the file was opened directly)
if __name__ == "__main__":
    pygame.init()
    game.main()
