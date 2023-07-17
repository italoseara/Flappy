from gameengine.engine import Engine


class Animation:
    # SPRITESHEET_MODE = enum.auto()
    # ASSETS_MODE = enum.auto()

    animations = {}

    def __init__(self, fps, *frames):
        self.frames = frames
        self.__pause = False
        self.fps = fps
        self.__count_dt = 0
        self.frame_index = 0

    @property
    def current_frame(self):
        return self.frames[self.frame_index]

    @property
    def pause(self): return self.__pause

    def pause(self):
        self.__pause = True
    
    def unpause(self):
        self.__pause = False

    def update(self):
        if not self.__pause:
            self.__count_dt += Engine.deltatime
            while self.__count_dt >= (static_dt := 1 / self.fps):
                self.__count_dt -= static_dt
                self.frame_index += 1
            self.frame_index %= len(self.frames)

    @classmethod
    def from_assets(cls, fps, *assets):
        return cls(fps, *assets)
