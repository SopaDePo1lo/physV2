import math
import pygame

SCRSIZEX, SCRSIZEY = 1600,900

black = (0, 0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0, 255)
blue = (0,0,255,255)
green = (0, 255 , 0)
red = (255 , 0, 0)
grey = (10,10,10,255)

g = 9.8
Pressure = 10
FINAL_PRESSURE = 5
ks = 4
kd = 0.5
#
dt = 0.005

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

class Point: #simple point class

    x = int
    y = int

    f = Vector
    v = Vector(0, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, black, (self.x, self.y), 1)

class Ball:

    x = int
    y = int

    mass = 1
    volume = 0

    points = []
    springs = []

    def __init__(self, x, y, nump, radius):
        self.x = x
        self.y = y
        for i in range(nump):
            point = Point(0,0)
            point.x = radius * math.sin(i * (2.0 * 3.14) / nump) + x
            point.y = radius * math.cos(i * (2.0 * 3.14) / nump) + y
            self.points.append(point)
            self.springs.append(Spring((0, 0), 0))

        for i in range(nump-1):
            self.addSpring(i, i, i+1)
        self.addSpring(nump-1, nump-1, 0)

    def addSpring(self, pi, i, j):
        self.springs[pi].indexes = (i, j)
        self.springs[pi].length = math.sqrt(((self.points[i].x - self.points[j].x)**2) + ((self.points[i].y - self.points[j].y)**2))

    def draw(self, screen):
        for point in self.points:
            pygame.draw.rect(screen, black, (point.x, point.y, 1, 1))

    def update(self):
        for point in self.points:
            fx = 0
            fy = self.mass*g*(abs(Pressure - FINAL_PRESSURE))
            point.f = Vector(fx, fy)

        for spring in self.springs:
            p1, p2 = spring.indexes
            x1 = self.points[p1].x
            y1 = self.points[p1].y
            x2 = self.points[p2].x
            y2 = self.points[p2].y

            r12d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            if r12d != 0:

                vx12 = self.points[p1].v.x - self.points[p2].v.x
                vy12 = self.points[p1].v.y - self.points[p2].v.y

                f = (r12d - spring.length) * ks + (vx12 * (x1 - x2) + vy12 * (y1 - y2)) * kd / r12d #i myself don't understand this formula

                Fx = ((x1 - x2) / r12d) * f
                Fy = ((y1 - y2) / r12d) * f
                self.points[p1].f.x -= Fx
                self.points[p1].f.y -= Fy
                self.points[p2].f.x += Fx
                self.points[p2].f.y += Fy

            spring.nv.x = (y1 - y2) / r12d
            spring.nv.y = -(x1 - x2) / r12d

        for spring in self.springs:
            p1, p2 = spring.indexes
            x1 = self.points[p1].x
            y1 = self.points[p1].y
            x2 = self.points[p2].x
            y2 = self.points[p2].y
            r12d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            pressurev = r12d * Pressure * (1.0/self.Volume())

            self.points[p1].f.x += spring.nv.x*pressurev
            self.points[p1].f.y += spring.nv.y*pressurev
            self.points[p2].f.x += spring.nv.x*pressurev
            self.points[p2].f.y += spring.nv.y*pressurev

        for p in self.points:
            # x
            p.v.x += (p.f.x / self.mass) * dt
            p.x += p.v.x * dt

            # boundaries y
            if p.x > SCRSIZEX:
                p.x = SCRSIZEX
                p.vx = -p.v.x

            # y
            p.v.y += p.f.y * dt
            p.y += p.v.y * dt

            # boundaries y
            if p.y > SCRSIZEY:
                p.y = SCRSIZEY
                p.v.y = -0.1*p.v.y

    def Volume(self):
        self.volume = 1
        for spring in self.springs:
            p1, p2 = spring.indexes
            x1 = self.points[p1].x
            y1 = self.points[p1].y
            x2 = self.points[p2].x
            y2 = self.points[p2].y
            r12d = math.sqrt((x1-x2)**2 + (y1-y2)**2)

            self.volume += 0.5 * abs(x1 - x2) * abs(spring.nv.x) * r12d
        return self.volume

    def IntegrateEuler(self):
        for point in self.points:
            dry = float
            point.v.x = point.v.x + (point.f.x / self.mass) * dt
            point.x = point.x + point.v.x*dt

            point.v.y = point.v.y + point.f.y * dt
            dry = point.v.y * dt

            if point.y + dry < 900: # less than screen size
                dry = -900 - point.y
                point.v.y = -0.1 * point.v.y

            point.y = -(point.y + dry)

    def draw_point_forces(self, screen):
        for point in self.points:
            x, y = point.x, point.y
            px = point.v.x
            py = point.v.y
            pygame.draw.aaline(screen, red, (x, y), (x+px, y+py))


class Spring:

    indexes = tuple
    lenght = float
    nv = Vector(0, 0)

    def __init__(self, indexes, lenght):
        self.indexes = indexes
        self.length = lenght
        # nx, ny = normal_vector
        # nv = Vector(nx, ny)

class Rect:

    x = int
    y = int
    width = int
    height = int

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def point_in(self, point):
        if (self.x < point.x < self.x+self.width) and (self.y < point.y < self.y+self.height):
            return True
        else:
            return False

    def draw(self, screen):
        pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height))

class Circle:

    x = int
    y = int
    radius = float

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def point_in(self, point):
        mx = point.x - self.x
        my = point.y - self.y
        if (mx**2 + my**2) < r**2:
            return True
        else:
            return False

    def draw(self, screen):
        pygame.draw.circle(screen, black, (self.x, self.y), self.radius, width=1)

class Rigidbody:

    type = object
    x = int
    y = int

    mass = float
    velocity = Vector
    acceleration = float

    orientation = float #angle in radians
    angularVelocity = float
    torque = float

    def __init__(self, x, y, type, mass):
        self.x = x
        self.y = y
        self.type = type
        self.mass = mass

class Object: #class for a physical object

    type = object #the type of object like a circle, a square or even a polygon
    x = int
    y = int

    #just some states
    on_floor = False

    #physical properties of objects
    mass = float
    rotation = float
    velocity = Vector

    def __init__(self, x, y, type, mass):
        self.x = x
        self.y = y
        self.type = type
        self.mass = mass

    def draw_forces(self, screen):
        F = self.mass*g
        if self.type == Rect:
            x = self.x + self.type.width/2
            y = self.y + self.type.height/2
            pygame.draw.aaline(screen, green, (x, y), (x, y+F))
        else:
            pygame.draw.aaline(screen, green, (self.x, self.y), (self.x, self.y+F))

    def draw(self, screen):
        self.type.draw(screen)
