class DeltaTime:
    value = 0
    @staticmethod
    def process(pygame_delta):
        DeltaTime.value = pygame_delta / 1000

    @staticmethod
    def get():
        return DeltaTime.value
