class HierarchicalObject:
    parent = None
    program = None

    def __init__(self):
        self.children = []

    def add_children(self, *children):
        for child in children:
            self.children.append(child)
            child.parent = self

    def remove_children(self, *children):
        for child in children:
            child.kill()

    def kill(self):
        if self.parent is not None:
            self.parent.children.remove(self)

    def update(self):
        if not self.program.request_quit:
            for child in list(self.children):
                child.update()

    def draw(self):
        for child in self.children:
            child.draw()

    @property
    def surface(self):
        return self.parent.surface

    @property
    def active(self):
        return bool(sum(child.active for child in self.children))

    @active.setter
    def active(self, value):
        for child in self.children:
            child.active = value

    @property
    def visible(self):
        return bool(sum(child.visible for child in self.children))

    @visible.setter
    def visible(self, value):
        for child in self.children:
            child.active = value
