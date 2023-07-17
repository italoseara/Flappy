from gameengine.engine import Engine


class Animation:
    # SPRITESHEET_MODE = enum.auto()
    # ASSETS_MODE = enum.auto()

    animations = {}

    def __init__(self, fps, *frames):
        self.frames = frames
        self.fps = fps
        self.__pause = False
        self.__count_dt = 0
        self.frame_index = 0

    @property
    def current_frame(self):
        return self.frames[self.frame_index].copy()

    @property
    def paused(self): return self.__pause

    def pause(self):
        self.__pause = True
    
    def unpause(self):
        self.__pause = False

    def update(self, child):
        if not self.__pause:
            self.__count_dt += child.program.time.delta
            while self.__count_dt >= (static_dt := 1 / self.fps):
                self.__count_dt -= static_dt
                self.frame_index += 1
                child.surface = self.current_frame
            self.frame_index %= len(self.frames)

    @classmethod
    def from_assets(cls, fps, *assets):
        return cls(fps, *assets)
