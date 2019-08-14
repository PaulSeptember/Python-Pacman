class Animation(object):
    def __init__(self, name):
        self.name = name
        self.frames = []
        self.col = 0
        self.forward = True
        self.speed = 0
        self.dt = 0.
        self.finished = False

    def add_frame(self, frame):
        self.frames.append(frame)

    def get_frame(self):
        return self.frames[self.col]

    def next_frame(self, dt):
        self.dt += dt
        if self.dt >= 1.0 / self.speed:
            if self.forward:
                self.col += 1
            else:
                self.col -= 1
            self.dt = 0.

    def loop(self, dt):
        self.next_frame(dt)
        if self.forward:
            if self.col == len(self.frames):
                self.col = 0
        else:
            if self.col == -1:
                self.col = len(self.frames) - 1

    def one_pass(self, dt):
        self.next_frame(dt)
        if self.forward:
            if self.col == len(self.frames):
                self.col = len(self.frames) - 1
                self.finished = True
        else:
            if self.col == -1:
                self.col = 0
                self.finished = True

    def ping(self, dt):
        self.next_frame(dt)
        if self.forward:
            if self.col == len(self.frames):
                self.col = 0
                self.forward = False
        else:
            if self.col == -1:
                self.col = 0
                self.forward = True

    def get_image(self, frame_number):
        return self.frames[frame_number]


class AnimationGroup(object):
    def __init__(self):
        self.animations = []
        self.animation = None
        self.col = 0

    def add(self, animation):
        self.animations.append(animation)

    def set_animation(self, name, col):
        self.animation = self.get_animation(name)
        self.animation.col = col

    def get_animation(self, name):
        for animation in self.animations:
            if animation.name == name:
                return animation
        return None

    def loop(self, dt):
        self.animation.loop(dt)
        return self.animation.get_frame()

    def one_pass(self, dt):
        self.animation.one_pass(dt)
        return self.animation.get_frame()

    def ping(self, dt):
        for i in self.animations:
            i.ping(dt)
        return self.animation.get_frame()

    def get_image(self):
        return self.animation.get_frame()
