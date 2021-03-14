import pygame
import math

class Point:
    x = 0
    y = 0
    static = False

    v = 0.0

    f = 0.0

    def __init__(self, xy, v, f):
        self.x, self.y = xy
        vx, vy = v
        fx, fy = f
        self.v = Vector(vx, vy)
        self.f = Vector(fx, fy)

class Vector: #simple vector class, might update in future if needed

    x = int
    y = int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def lenght(self):
        return math.sqrt(x**2 + y**2)

    def lenght2(self): #in some cases you don't need the square root
        return (x**2 + y**2)

class DoublePendulum:

    pos0 = Point(0, 0)

    #mass
    m1 = int
    m2 = int

    #lengths
    l1 = float
    l2 = float

    #angles
    a1 = float
    a2 = float

    

    def __init__(self, pos0, m1, m2, l1, l2, alpha1, alpha2):
        x0, y0 = pos0
        self.pos0 = Point(x0, y0)
        self.m1 = m1
        self.m2 = m2
        self.l1 = l1
        self.l2 = l2
        self.a1 = alpha1
        self.a2 = alpha2
