from .basenode import BaseNode


class Timer(BaseNode):
    def __init__(self, target_time, auto_pause=True):
        super().__init__()
        self.auto_pause = auto_pause
        self.target_time = target_time
        self.current_time = 0
        self.reached = 0
        self.__pause = False

    @property
    def paused(self):
        return self.__pause

    def pause(self):
        self.__pause = True

    def unpause(self):
        self.__pause = False

    def update(self):
        super().update()
        self.reached = 0
        if not self.__pause:
            self.current_time += self.program.time.delta
            if self.current_time >= self.target_time:
                self.reached += int(self.current_time / self.target_time)
                self.current_time -= self.reached * self.target_time
                self.__pause = self.auto_pause
