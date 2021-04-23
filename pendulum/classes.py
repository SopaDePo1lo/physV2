import pygame
import math
from math import sin, cos

g = 9.8
dt = 0.0225

class Point:
    x = 0
    y = 0
    static = False

    def __init__(self, xy):
        self.x, self.y = xy

    def tuple(self):
        return (self.x, self.y)

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

    pos0 = Point((0, 0))

    #mass
    m1 = int
    m2 = int

    #lengths
    l1 = float
    l2 = float

    #angles
    a1 = float
    a2 = float

    #angle velocity and acceleration
    a1_v = 0.0
    a2_v = 0.0

    a1_a = 0.0
    a2_a = 0.0

    #force for integration with kinematic bodies
    f1 = Vector(0.0, 0.0)
    f2 = Vector(0.0, 0.0)

    def draw_point(self, screen, colour):
        x1 = self.l1 * math.sin(self.a1)
        y1 = self.l1 * math.cos(self.a1)

        x2 = self.l2 * math.sin(self.a2) + x1
        y2 = self.l2 * math.cos(self.a2) + y1
        pygame.draw.circle(screen, colour, (self.pos0.x+x2, self.pos0.y+y2), 1)

    def calculate_motion(self):
        top1 = -g*(2*self.m1 +self.m2)*sin(self.a1)
        top2 = self.m2*g*sin(self.a1-2*self.a2)
        top3 = 2*sin(self.a1-self.a2)*self.m2*((self.a2_v**2)*self.l2 + (self.a1_v**2)*self.l1*cos(self.a1-self.a2))
        num1 = -g*(2*self.m1+self.m2)*math.sin(self.a1) - self.m2*g*math.sin(self.a1-2*self.a2)-2*math.sin(self.a1-self.a2)*self.m2*(self.a2_v**2*self.l2 + self.a1_v**2*self.l1*math.cos(self.a1-self.a2))
        num2 = self.l1*(2*self.m1 + self.m2 - self.m2*math.cos(2*self.a1- 2*self.a2))
        self.a1_a = (top1-top2-top3)/num2

        p1 = 2*math.sin(self.a1-self.a2)
        p2 = (self.a1_v**2)*self.l1*(self.m1+self.m2)
        p3 = g*(self.m1 + self.m2)*math.cos(self.a1)
        p4 = (self.a2_v**2)*self.l2*self.m2*math.cos(self.a1-self.a2)
        p5 = self.l2*(2*self.m1 + self.m2 - self.m2*math.cos(2*self.a1 - 2*self.a2))
        self.a2_a = p1*(p2+p3+p4)/p5
        pass

    def update(self):
        self.calculate_motion()
        self.f1 = (self.a1_a*self.m1, self.a1_a*self.m1)
        self.f2 = (self.a2_a*self.m2, self.a2_a*self.m2)
        self.a1_v += self.a1_a*dt
        self.a2_v += self.a2_a*dt
        self.a1 += self.a1_v*dt
        self.a2 += self.a2_v*dt

    def draw(self, screen, colour):
        x1 = self.l1 * math.sin(self.a1)
        y1 = self.l1 * math.cos(self.a1)

        x2 = self.l2 * math.sin(self.a2) + x1
        y2 = self.l2 * math.cos(self.a2) + y1


        pygame.draw.aaline(screen, colour, (self.pos0.tuple()), (self.pos0.x+x1, self.pos0.y+y1))
        pygame.draw.aaline(screen, colour, (self.pos0.x+x1, self.pos0.y+y1), (self.pos0.x+x2, self.pos0.y+y2))
        pygame.draw.circle(screen, colour, (self.pos0.x+x1, self.pos0.y+y1), 5)
        pygame.draw.circle(screen, colour, (self.pos0.x+x2, self.pos0.y+y2), 5)
        pass

    def __init__(self, pos0, m1, m2, l1, l2, alpha1, alpha2):
        x0, y0 = pos0
        self.f1 = Vector(0.0, 0.0)
        self.f2 = Vector(0.0, 0.0)
        self.pos0 = Point((x0, y0))
        self.m1 = m1
        self.m2 = m2
        self.l1 = l1
        self.l2 = l2
        self.a1 = alpha1
        self.a2 = alpha2
