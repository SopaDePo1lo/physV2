import math
import pygame
import kinematic.collision as fn

SCRSIZEX, SCRSIZEY = 1600,900

g = 9.8
ks = 4
kd = 0.5
dt = 0.05

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

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen, colour):
        pygame.draw.circle(screen, black, (self.x, self.y), 1)

    def tuple(self):
        return (self.x, self.y)

class Rect:

    x = int
    y = int
    width = int
    height = int

    #phys variables
    v = Vector(0.0, 0.0)
    f = Vector(0.0, 0.0)
    mass = float
    friction = 0.005

    #STATES
    static = False

    def __init__(self, x, y, width, height, mass):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = mass
        self.v = Vector(0.0, 0.0)
        self.f = Vector(0.0, 0.0)

    def draw_forces(self, screen, colour):
        pass

    def gravity(self):
        if self.static==False:
            self.f.x = 0
            self.f.y = self.mass * 9.8

    def IntegrateEuler(self, arr):
        if self.static==False:
            self.v.x += (self.f.x/self.mass)*dt
            self.x += self.v.x*dt
            if self.x > SCRSIZEX:
                self.x = SCRSIZEX
                self.v.x = -self.v.x
            elif self.x < 0:
                self.x=0
                self.v.x = -self.v.x
            for object in arr:
                if fn.collision(self, arr):
                    self.x -= self.v.x*dt
                    # self.v.x = -0.5*self.v.x

            self.v.y += (self.f.y/self.mass) * dt
            self.y += self.v.y * dt

            if self.y > SCRSIZEY:
                self.y = SCRSIZEY
                self.v.y = -0.2*self.v.y
            elif self.y < 0:
                self.y = 0
                self.v.y = -0.2*self.v.y
            for object in arr:
                if fn.collision(self, arr):
                    self.y -= self.v.y*dt
                    self.v.y = -0.2*self.v.y

    def update(self, arr):
        self.gravity()
        self.IntegrateEuler(arr)

    def point_in(self, point):
        if (self.x < point.x < self.x+self.width) and (self.y < point.y < self.y+self.height):
            return True
        else:
            return False

    def coords_in(self,coords):
        x, y = coords
        if (self.x < x < self.x+self.width) and (self.y < y < self.y+self.height):
            return True
        else:
            return False

    def draw(self, screen, colour):
        pygame.draw.rect(screen, colour, (self.x, self.y, self.width, self.height))

class Circle:

    x = int
    y = int
    radius = float

    #phys variables
    v = Vector(0.0, 0.0)
    f = Vector(0.0, 0.0)
    mass = float

    #STATES
    static = False

    def __init__(self, x, y, radius, mass):
        self.x = x
        self.y = y
        self.radius = radius

        self.v = Vector(0.0, 0.0)
        self.f = Vector(0.0, 0.0)
        self.mass = mass

    def gravity(self):
        if self.static==False:
            self.f.x = 0
            self.f.y = self.mass * 9.8

    def IntegrateEuler(self, arr):
        if self.static==False:
            self.v.x += (self.f.x/self.mass)*dt
            self.x += self.v.x*dt
            if self.x > SCRSIZEX:
                self.x = SCRSIZEX
                self.v.x = -0.2*self.v.x
            elif self.x < 0:
                self.x=0
                self.v.x = -0.2*self.v.x
            for object in arr:
                if fn.collision(self, arr):
                    self.x -= self.v.x*dt
                    # self.v.x = -0.5*self.v.x
                    continue

            self.v.y += (self.f.y/self.mass) * dt
            self.y += self.v.y * dt

            if self.y > SCRSIZEY:
                self.y = SCRSIZEY
                self.v.y = -0.2*self.v.y
            elif self.y < 0:
                self.y = 0
                self.v.y = -0.2*self.v.y
            for object in arr:
                if fn.collision(self, arr):
                    self.y -= self.v.y*dt
                    self.v.y = -0.5*self.v.y
                    continue

    def update(self, arr):
        self.gravity()
        self.IntegrateEuler(arr)

    def draw_forces(self, screen, colour):
        pygame.draw.aaline(screen, colour, (self.x, self.y), (self.x+self.v.x, self.y+self.v.y))

    def point_in(self, point):
        mx = point.x - self.x
        my = point.y - self.y
        if (mx**2 + my**2) < self.radius**2:
            return True
        else:
            return False

    def coords_in(self, coords):
        x, y = coords
        mx = x - self.x
        my = y - self.y
        if (mx**2 + my**2) < self.radius**2:
            return True
        else:
            return False

    def draw(self, screen, colour):
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius, width=1)
        # pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)
