from __future__ import annotations
import math

from glm.vec.vec2 import Vec2


class Vec3(Vec2):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self.z = z

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other: Vec3) -> Vec3:
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other: Vec3) -> Vec3:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, other: Vec3) -> Vec3:
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __imul__(self, other: Vec3) -> Vec3:
        self.x *= other.x
        self.y *= other.y
        self.z *= other.z
        return self

    def __truediv__(self, other: float) -> Vec3:
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __itruediv__(self, other: Vec3) -> Vec3:
        self.x /= other.x
        self.y /= other.y
        self.z /= other.z
        return self

    def __mod__(self, other: Vec3) -> Vec3:
        return Vec3(self.x % other.x, self.y % other.y, self.z % other.z)

    def __imod__(self, other: Vec3) -> Vec3:
        self.x %= other.x
        self.y %= other.y
        self.z %= other.z
        return self

    def __neg__(self) -> Vec3:
        return Vec3(-self.x, -self.y, -self.z)

    def __eq__(self, other: Vec3) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> Vec3:
        return self / self.length()

    @staticmethod
    def dot(v1: Vec3, v2: Vec3) -> float:
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    @staticmethod
    def cross(v1: Vec3, v2: Vec3) -> Vec3:
        return Vec3(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x)
