from glm.camera import Camera
from glm.vec.vec3 import Vec3

exCam = Camera(90.0, 0.1, 100000)
exCam.lookAt(Vec3(0, 0, 1))
exCam.teleport(Vec3(10, 10, 10))
exCam.teleport(Vec3(5, 5, 5))
exCam.move(Vec3(1, 1, 1))
exCam.move(Vec3(1, 1, 1))
exCam.move(Vec3(1, 1, 1))
exCam.move(Vec3(1, 1, 1))

print(exCam.pos.x, exCam.pos.y, exCam.pos.z)
print(exCam.dir.x, exCam.dir.y, exCam.dir.z)
