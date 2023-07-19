from .timer import Timer


class Animation(Timer):
    # SPRITESHEET_MODE = enum.auto()
    # ASSETS_MODE = enum.auto()

    animations = {}

    def __init__(self, fps, *frames):
        super().__init__(1 / fps, False)
        self.frames = frames
        self.fps = fps
        self.__pause = False
        self.frame_index = 0

    @property
    def current_frame(self):
        return self.frames[self.frame_index].copy()

    def update(self, child):
        super().update()
        for _ in range(self.reached):
            self.frame_index += 1
            self.frame_index %= len(self.frames)
            child.surface = self.current_frame

    @classmethod
    def from_assets(cls, fps, *assets):
        return cls(fps, *assets)
