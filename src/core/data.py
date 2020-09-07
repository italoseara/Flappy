class FrameManager:
    """Manages a list of frames."""
    def __init__(self, frames, current_index=0):
        self.frame_list = list(frames)
        self.current_index = current_index

    @property
    def current_frame(self):
        return self.frame_list[self.current_index]
