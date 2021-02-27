import math
import pygame

black = (0, 0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0, 255)
blue = (0,0,255,255)
green = (0, 255 , 0)
red = (255 , 0, 0)
grey = (10,10,10,255)

g = 0.98
ks = 755
kd = 35

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

class Spring:

    indexes = tuple
    lenght = float
    nv = Vector(0, 0)

    def __init__(self, indexes, lenght):
        self.indexes = indexes
        self.lenght = lenght
        # nx, ny = normal_vector
        # nv = Vector(nx, ny)

class Rope:

    points = []
    springs = []
    mass = 0.01

    def __init__(self, arr):
        self.points = arr
        for i in range(len(arr)-1):
            dx = arr[i].x - arr[i+1].x
            dy = arr[i].y - arr[i+1].y
            lenght = math.sqrt(dx**2 + dy**2)
            indexes = (i, i+1)
            self.springs.append(Spring(indexes, lenght))

    def update(self):
        for point in self.points:
            fx = 0
            fy = self.mass*g
            point.f = Vector(fx, fy)

        for i in range(len(self.springs)):
            p1, p2 = self.springs[i].indexes
            x1 = self.points[p1].x
            y1 = self.points[p1].y
            x2 = self.points[p2].x
            y2 = self.points[p2].y

            r12d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            if r12d != 0:

                vx12 = self.points[p1].v.x - self.points[p2].v.x
                vy12 = self.points[p1].v.y - self.points[p2].v.y

                f = (r12d - self.springs[i].lenght) * ks + (vx12 * (x1 - x2) + vy12 * (y1 - y2)) * kd / r12d #i myself don't understand this formula

                Fx = ((x1 - x2) / r12d) * f
                Fy = ((y1 - y2) / r12d) * f
                self.points[p1].f.x -= Fx
                self.points[p1].f.y -= Fy
                self.points[p2].f.x += Fx
                self.points[p2].f.y += Fy

                self.springs[i].nv.x = (y1 - y2) / r12d
                self.springs[i].nv.y = -(x1 - x2) / r12d

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
