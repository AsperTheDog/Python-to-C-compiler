from glm.vec.vec3 import Vec3


class Camera:
    def __init__(self, FOV: float, near: float, far: float):
        self.fov = FOV
        self.near = near
        self.far = far

        self.pos = Vec3(0, 0, 0)
        self.dir = Vec3(0, 0, -1)

    def lookAt(self, newDir: Vec3) -> None:
        self.dir = newDir

    def anchor(self, obj: Vec3) -> None:
        self.dir = obj - self.pos

    def move(self, offset: Vec3) -> None:
        self.pos += offset

    def teleport(self, newPos: Vec3) -> None:
        self.pos = newPos
