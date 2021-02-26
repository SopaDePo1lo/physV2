import math
import pygame

black = (0, 0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0, 255)
blue = (0,0,255,255)
green = (0, 255 , 0)
red = (255 , 0, 0)
grey = (10,10,10,255)

g = 9.8

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
