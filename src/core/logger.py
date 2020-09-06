import sys

class Logger:
    _prefix = ""

    @staticmethod
    def set_prefix(prefix):
        Logger._prefix = str(prefix)

    @staticmethod
    def log(msg, end='\n'):
        print(Logger._prefix + msg, file=sys.stderr, end=end)
