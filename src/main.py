import sys
import platform

major_version = platform.python_version()[0]
if not (major_version == "3"):
    print(f"Major python version needs to be 3 (current is {major_version}).", file=sys.stderr)
    sys.exit(1)

import core
import game

if __name__ == "__main__":
    game.main()
