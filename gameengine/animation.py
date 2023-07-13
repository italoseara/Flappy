from gameengine.engine import Engine


class Animation:
    # SPRITESHEET_MODE = enum.auto()
    # ASSETS_MODE = enum.auto()

    animations = {}

    def __init__(self, fps, *frames):
        self.frames = frames
        self.fps = fps
        self.__static_dt = 1 / self.fps
        self.__count_dt = 0
        self.__current_frame = 0

    @property
    def current_frame(self):
        return self.frames[self.__current_frame]

    def update(self):
        self.__count_dt += Engine.deltatime
        while self.__count_dt >= self.__static_dt:
            self.__count_dt -= self.__static_dt
            self.__current_frame += 1
        self.__current_frame %= len(self.frames)

    @classmethod
    def from_assets(cls, fps, *assets):
        return cls(fps, *assets)
