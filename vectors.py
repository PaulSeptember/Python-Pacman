from math import sqrt


class Vector2D(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.x, self.y

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def magnitude_squared(self):
        return self.x**2 + self.y**2

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar):
        return Vector2D(self.x // scalar, self.y // scalar)

    # TODO: other 5 __ne__, __lt__, __le__, __gt__, __ge__
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __hash__(self):
        return id(self)

    def copy(self):
        return Vector2D(self.x, self.y)
