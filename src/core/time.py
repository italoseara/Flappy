class DeltaTime:
    value = 1
    @classmethod
    def process(cls, pygame_delta):
        cls.value = pygame_delta / 1000

    @classmethod
    def get(cls):
        return cls.value
