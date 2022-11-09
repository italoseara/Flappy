class Animations:
    animations = {}

    def __init__(self, fps, *frames):
        self.frames = frames
        self.fps = fps
        self.dt = 1 / fps
        self.current_time = 0
        self.current_frame = 0

    def get_current_frame(self):
        return self.frames[self.current_frame]

    def update(self, deltatime, reverse=False):
        self.current_time += deltatime
        if self.current_time >= self.dt:
            self.current_time -= self.dt
            if reverse:
                to_add = -1
            else:
                to_add = 1
            self.current_frame = (self.current_frame + to_add) % len(self.frames)

    @classmethod
    def add_animation_data(cls, name, type, *args):
        if name not in cls.animations.keys():
            cls.animations[name] = []
        cls.animations[name].append({"type": type, "data": args})

    @classmethod
    def get_animation_data(cls, name):
        return cls.animations[name]

    @classmethod
    def get_animation(cls, name, fps):
        surfaces = []
        for animation_data in cls.get_animation_data(name):
            animation_type = animation_data["type"]
            data = animation_data["data"]
            if animation_type == "frame":
                surfaces.append(data[0])
        return cls(fps, *surfaces)
