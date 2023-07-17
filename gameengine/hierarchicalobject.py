class HierarchicalObject:
    parent = None
    program = None

    def __init__(self) -> None:
        self.children = []

    def add_children(self, *children):
        for child in children:
            self.children.append(child)
            child.parent = self

    def remove_child(self, *children):
        for child in children:
            self.children.remove(child)

    def kill(self):
        if self.parent is not None:
            self.parent.children.remove(self)

    def update(self):
        for child in list(self.children):
            child.update()

    def draw(self):
        for child in self.children:
            child.draw()
