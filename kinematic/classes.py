import math
import pygame
import kinematic.collision as fn

screenx, screeny = 1600,900

g = 9.8
ks = 4
kd = 0.5
dt = 0.05

def check_screen_boundary(object):
    if object.position.x > screenx:
        object.position.x = screenx
        object.velocity.x = -object.velocity.x
    elif object.position.x < 0:
        object.position.x = 0
        object.velocity.x = -object.velocity.x

    if object.position.y > screeny:
        object.position.y = screeny
        object.velocity.y = -object.velocity.y
    elif object.position.y < 0:
        object.position.y = 0
        object.velocity.y = -object.velocity.y

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

    def tuple(self):
        return (self.x, self.y)

class Rect:

    position = Vector

    width = int
    height = int

    static=False

    mass = float
    force = Vector
    velocity = Vector

    def __init__(self, pos, width, height, mass, static=False):
        x, y = pos
        self.position = Vector(x,y)
        self.height = height
        self.width = width
        self.mass = mass
        self.static = static
        self.force = Vector(0,0)
        self.velocity = Vector(0,0)

    def coords_in(self, pos):
        x, y = pos
        if (self.position.x < x < self.position.x+self.width) and (self.position.y < y < self.position.y+self.height):
            return True
        else:
            return False

    def gravity(self):
        self.force.x = 0
        self.force.y = self.mass*g

    def IntegrateEuler(self, array):
        self.velocity.x += self.force.x/self.mass*dt
        self.position.x += self.velocity.x*dt

        if fn.collision(self, array):
            self.position.x -= self.velocity.x*dt

        self.velocity.y += self.force.y/self.mass*dt
        self.position.y += self.velocity.y*dt

        if fn.collision(self, array):
            self.position.y -= self.velocity.y*dt

    def update(self, array):
        if self.static == False:
            self.gravity()
            self.IntegrateEuler(array)
            check_screen_boundary(self)

    def draw(self, screen, colour):
        pygame.draw.rect(screen, colour, (self.position.x, self.position.y, self.width, self.height))
