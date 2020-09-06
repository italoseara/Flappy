from __future__ import print_function
import sys
import platform
import os

# TODO: logger

# check if python version is 3.7+ (needed)
# still, this file should be python2-compliant for the check to run.
major, minor = sys.version_info[:2]
if sys.version_info < (3, 7):
    print("You need to use at least python 3.7 (current is ~{}.{})".format(major, minor), file=sys.stderr)
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
