from math import sqrt, sin, cos, acos, pi
from dataclasses import dataclass


@dataclass
class Vector:
    x: float
    y: float

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __sub__(self, other):
        return self + (-other)

    def __abs__(self):
        return sqrt(self.x**2 + self.y**2)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def rotate(self, fi: float):
        x, y = self.x, self.y
        self.x = x * cos(fi) - y * sin(fi)
        self.y = x * sin(fi) + y * cos(fi)


def get_angle(a: Vector, b: Vector) -> float:
    return acos(a * b / (abs(a) * abs(b)))


def elipse_generator(a: Vector, b: Vector, r: float, points_num: int = 10):
    """
    Generate `points_num` of points on elipse with focuses `a` and `b` and summ `r`.
    For this I use parametric form of elipse func: x = l * sin(t), y = s * cos(t),
    where l = r / 2, s = sqrt(r ** 2 - abs(b - a) ** 2) / 2.
    """
    l = r / 2
    s = sqrt(r ** 2 - abs(b - a) ** 2) / 2
    angle = get_angle(b - a, Vector(1, 0))

    if (b - a).y < 0:
        angle = 2 * pi - angle

    for i in range(points_num):
        t = 2 * pi / points_num * i
        x = l * sin(t)
        y = s * cos(t)
        v = Vector(x, y)
        v.rotate(angle)
        v += Vector((a + b).x / 2, (a + b).y / 2)
        yield v
