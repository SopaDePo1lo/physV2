import math
import pygame
import functions as fn

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
dt = 0.01

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

    def draw(self, screen):
        pygame.draw.circle(screen, black, (self.x, self.y), 1)

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

    def coords_in(self,coords):
        x, y = coords
        if (self.x < x < self.x+self.width) and (self.y < y < self.y+self.height):
            return True
        else:
            return False

    # def update(self):
    #     if not self.static:
    #         self.y+=1
    #     else:
    #         pass

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

    # def update(self):
    #     if not self.static:
    #         self.y+=1
    #     else:
    #         pass

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

    def draw(self, screen):
        pygame.draw.circle(screen, black, (self.x, self.y), self.radius, width=1)

class Object: #class for a physical object

    type = object #the type of object like a circle, a square or a polygon
    x = int
    y = int

    #just some states
    on_floor = False
    static = False

    v = Vector(0,0)
    f = Vector(0,0)
    ef = Vector(0,0)

    #physical properties of objects
    mass = float
    rotation = float
    velocity = Vector


    def __init__(self, x, y, type, mass, static):
        self.x = x
        self.y = y
        self.type = type
        self.mass = mass
        self.static = static
        self.v = Vector(0,0)
        self.f = Vector(0,0)
        self.ef = Vector(0,0)

    def external_forces(self, vec):
        self.ef.x = vec.x
        self.ef.y = vec.y

    def all_forces(self):
        self.f.x=self.ef.x
        self.f.y+=self.ef.y

    def update_type_coords(self):
        self.type.x = self.x
        self.type.y = self.y

    def update(self, arr):
        if not self.static:
            self.gravity()
            self.all_forces()
            self.IntegrateEuler(arr)
        self.update_type_coords()

    def gravity(self):
        self.f.y=self.mass*g

    def IntegrateEuler(self, arr):
        self.v.x +=(self.f.x/self.mass)*dt
        self.x += self.v.x*dt
        if fn.collision(self, arr):
            self.x -= self.v.x*dt
            self.v.x = -self.v.x

        self.v.y += (self.f.y/self.mass)*dt
        self.y += self.v.y*dt
        if fn.collision(self, arr):
            self.y -= self.v.y*dt
            self.v.y = -self.v.y

    def draw_forces(self, screen):
        if self.type == Rect:
            x = self.x + self.type.width/2
            y = self.y + self.type.height/2
            pygame.draw.aaline(screen, green, (x, y), (x+self.f.x, y+self.f.y))
        else:
            pygame.draw.aaline(screen, green, (self.x, self.y), (self.x+self.v.x, self.y+self.v.y))

    def coords_in(self, coords):
        return self.type.coords_in(coords)

    def draw(self, screen):
        self.type.draw(screen)
