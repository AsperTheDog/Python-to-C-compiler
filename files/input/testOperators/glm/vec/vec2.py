from __future__ import annotations
import math


class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Vec2) -> Vec2:
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Vec2) -> Vec2:
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: Vec2) -> Vec2:
        return Vec2(self.x * other.x, self.y * other.y)

    def __imul__(self, other: Vec2) -> Vec2:
        self.x *= other.x
        self.y *= other.y
        return self

    def __truediv__(self, other: float) -> Vec2:
        return Vec2(self.x / other, self.y / other)

    def __itruediv__(self, other: Vec2) -> Vec2:
        self.x /= other.x
        self.y /= other.y
        return self

    def __mod__(self, other: Vec2) -> Vec2:
        return Vec2(self.x % other.x, self.y % other.y)

    def __imod__(self, other: Vec2) -> Vec2:
        self.x %= other.x
        self.y %= other.y
        return self

    def __neg__(self) -> Vec2:
        return Vec2(-self.x, -self.y)

    def __eq__(self, other: Vec2) -> bool:
        return self.x == other.x and self.y == other.y

    def normalize(self) -> Vec2:
        return self / self.length()

    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    @staticmethod
    def dot(v1: Vec2, v2: Vec2) -> float:
        return v1.x * v2.x + v1.y * v2.y