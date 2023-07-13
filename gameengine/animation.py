from gameengine.engine import Engine


class Animation:
    # SPRITESHEET_MODE = enum.auto()
    # ASSETS_MODE = enum.auto()

    animations = {}

    def __init__(self, fps, *frames):
        self.frames = frames
        self.fps = fps
        self.__count_dt = 0
        self.frame_index = 0

    @property
    def current_frame(self):
        return self.frames[self.frame_index]

    def update(self):
        if self.fps is not None:
            self.__count_dt += Engine.deltatime
            while self.__count_dt >= (static_dt := 1 / self.fps):
                self.__count_dt -= static_dt
                self.frame_index += 1
            self.frame_index %= len(self.frames)

    @classmethod
    def from_assets(cls, fps, *assets):
        return cls(fps, *assets)
