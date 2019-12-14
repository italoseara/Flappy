"""Ferramentas de debug."""

class Logbook:
    """Um sistema básico de logging."""

    PREFIX = "\033[34mlog:\033[m"

    def __init__(self, enabled_at_startup=True):
        self.enabled = enabled_at_startup

    def log(self, *args, **kwargs):
        """Mostra informações no console."""
        if self.enabled:
            print(self.PREFIX, *args, **kwargs)
