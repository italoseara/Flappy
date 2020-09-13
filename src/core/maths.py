from __future__ import annotations

class Vector2:
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], tuple) and len(args[0]) == 2:
            self.x, self.y = args[0]
        elif len(args) == 1 and isinstance(args[0], Vector2):
            self.x = args[0].x
            self.y = args[0].y
        elif len(args) == 2:
            self.x, self.y = args
        else:
            raise TypeError(
                "could not find matching pattern for argument list: {}{}".format(
                    type(self).__name__,
                    args,
                )
            )

    def into_tuple(self) -> tuple:
        return (self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y

class Rectangle:
    def __init__(self, *args):
        if len(args) == 4:
            self.x, self.y, self.width, self.height = args
        elif len(args) == 1 and isinstance(args[0], tuple) and len(args[0]) == 4:
            self.x, self.y, self.width, self.height = args[0]
        elif len(args) == 1 and isinstance(args[0], Rectangle):
            self.x = args[0].x
            self.y = args[0].y
            self.width = args[0].width
            self.height = args[0].height
        elif (len(args) == 2
              and isinstance(args[0], tuple)
              and len(args[0]) == 2
              and isinstance(args[1], tuple)
              and len(args[1]) == 2):
            self.x, self.y = args[0]
            self.width, self.height = args[1]
        else:
            raise TypeError(
                "could not find matching pattern for argument list: {}{}".format(
                    type(self).__name__,
                    args,
                )
            )
