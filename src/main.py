from __future__ import print_function
import sys
import os
from pathlib import Path

# check if python version is 3.7+ (needed)
# still, this file should be python2-compliant for the check to run.
major, minor = sys.version_info[:2]
if sys.version_info < (3, 7):
    print(
        "You need to use at least python 3.7 (current is ~{}.{})".format(major, minor),
        file=sys.stderr,
    )
    sys.exit(1)

from core.logger import Logger

# import pygame and try to supress the annoying startup message.
Logger.log("Loading pygame...")
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

Logger.log("Pygame loaded.")

# start the game
if __name__ == "__main__":
    import game
    # Open or Create the data file if it does not exist
    data_path = (Path(__file__) / ".." / "data").resolve()
    audio_path = (Path(__file__) / ".." / "audio").resolve()
    data_path.mkdir(parents=True, exist_ok=True)
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    game.main(data_path, audio_path)
