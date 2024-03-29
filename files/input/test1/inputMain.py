import dirTest.dirFileTest
import dirTest.dirFileTest as test
from dirTest.dirFileTest import mul as externMul
from dirTest.dirFileTest import *

from dirTest import dirFileTest

x = 1
z = x
bb = 3.0
other = "String"


def mul(a: int, b: int) -> int:
    c = a * b
    return c


y = mul(1, 2)


class Multiplier:
    staticA = 2
    staticB = 3

    def __init__(self):
        self.a = 0
        self.b = 0

    def addAB(self, a: int, b: int):
        self.a = a
        self.b = b

    def mul(self) -> int:
        return mul(self.a, self.b)

    @staticmethod
    def staticMul() -> int:
        return mul(Multiplier.staticA, Multiplier.staticB)


mult = Multiplier()
mult.addAB(x, y)
mult2 = Multiplier()
mult2.addAB(y, z)


def example():
    print("example")
