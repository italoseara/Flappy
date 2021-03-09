class DeltaTime:
    def __init__(self):
        self.value = 0

    def process(self, pygame_delta):
        self.value = pygame_delta / 1000

    def get(self):
        return self.value
