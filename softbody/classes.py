import math
import pygame


SCRSIZEX, SCRSIZEY = 1600,900

ks = 4
kd = 0.5
dt = 0.05

class point:
    x = 0
    y = 0

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

class spring:
    i = 0
    j = 0

    length = 0.0

    nx = 0.0
    ny = 0.0

    def __init__(self, indx, length, n):
        self.i, self.j = indx
        self.length = length
        self.nx, self.ny = n

class slope:

    start = point((0,0),(0,0),(0,0))
    end = point((0,0),(0,0),(0,0))
    m = float

    def __init__(self, start, end):
        x1, y1 = start
        x2, y2 = end
        self.m = -(y2-y1)/(x2-x1)
        self.start = point((x1, y1), (0,0), (0,0))
        self.end = point((x2, y2), (0,0), (0,0))

    def get_y(self, x):
        x1 = x-self.start.x
        return x1*self.m

    def draw(self, screen, colour):
        pygame.draw.aaline(screen, colour, (self.start.x, self.start.y), (self.end.x, self.end.y))
        pygame.draw.aaline(screen, colour, (self.start.x, self.start.y), (self.end.x, self.start.y))
        pygame.draw.aaline(screen, colour, (self.end.x, self.start.y), (self.end.x, self.end.y))

    def point_in(self, point):
        x, y = point
        if self.start.x<=x<=self.end.x or self.start.x>=x>=self.end.x:
            ycol = self.start.y-self.get_y(x)
            if self.start.y>=y>=ycol:
                return True
        return False

class ball:

    pt_amount = 0
    points = []
    springs = []
    radius = 0.0
    mass = 1.0
    volume = 0.0
    pressure = 5.5 #default should be 10.0, if you want more buoyancy then set it to a lower value, if you want it more deflated then icrease the value !!MUST BE MORE THAN MAX_PRESSURE
    max_pressure = 3.0

    def __init__(self, points, x, y, radius, mass):
        for i in range(points):
            self.pt_amount = points
            self.radius = radius
            x1 = radius*math.sin(i * (2.0 * 3.14) / points) + x
            y1 = radius*math.cos(i * (2.0 * 3.14) / points) + y
            pt = point((x1, y1), (0.0, 0.0), (0.0, 0.0))
            self.mass = mass
            self.points.append(pt)

        for i in range(points):
            for j in range(i):
                if j != i:
                    self.addSpring(j,i)

    def addSpring(self,i,j):
        pA,pB = self.points[i],self.points[j]
        length = math.sqrt((pA.x - pB.x) *
                         (pA.x - pB.x) +
                         (pA.y - pB.y) *
                         (pA.y - pB.y))
        s = spring((i, j), length, (0,0))
        self.springs.append(s)


    def gravity(self):
        for point in self.points:
            point.f.x = 0
            point.f.y = self.mass * 9.8 *(self.pressure-self.max_pressure)

    def spring_linear_force(self):
        for spring in self.springs:
            i, j = spring.i, spring.j
            x1 = self.points[i].x
            y1 = self.points[i].y
            x2 = self.points[j].x
            y2 = self.points[j].y

            r12d = math.sqrt((x1 -x2)**2 + (y1-y2)**2)

            if r12d != 0:
                vx12 = self.points[i].v.x - self.points[j].v.x
                vy12 = self.points[i].v.y - self.points[j].v.y

            f = (r12d - spring.length)*ks + (vx12*(x1-x2) + vy12*(y1-y2))*kd/r12d

            fx = ((x1-x2)/r12d)*f
            fy = ((y1-y2)/r12d)*f

            self.points[i].f.x -= fx
            self.points[i].f.y -= fy
            self.points[j].f.x += fx
            self.points[j].f.y += fy

            spring.nx = (y1 - y2) / r12d
            spring.ny -(x1 - x2) / r12d

    def volume_calc(self):
        for spring in self.springs:
            i, j = spring.i, spring.j
            x1 = self.points[i].x
            y1 = self.points[i].y
            x2 = self.points[j].x
            y2 = self.points[j].y

            r12d = math.sqrt((x1 -x2)**2 + (y1-y2)**2)

            self.volume += 0.5*abs(x1-x2)*abs(spring.nx)*r12d
        return self.volume

    def pressure_force(self):
        for spring in self.springs:
            i, j = spring.i, spring.j
            x1 = self.points[i].x
            y1 = self.points[i].y
            x2 = self.points[j].x
            y2 = self.points[j].y

            r12d = math.sqrt((x1 -x2)**2 + (y1-y2)**2)
            pressurev = r12d*self.pressure*(float(1.)/self.volume_calc())

            self.points[i].f.x += spring.nx*pressurev
            self.points[i].f.y += spring.ny*pressurev
            self.points[j].f.x += spring.nx*pressurev
            self.points[j].f.y += spring.ny*pressurev

    def newtons_equation(self, arr):
        for point in self.points:
            point.v.x += (point.f.x/self.mass)*dt
            point.x += point.v.x*dt
            if point.x > SCRSIZEX:
                point.x = SCRSIZEX
                point.v.x = -point.v.x
            elif point.x < 0:
                point.x=0
                point.v.x = -point.v.x
            for slope in arr:
                if slope.point_in((point.x, point.y)):
                    point.x -= point.v.x*dt
                    point.v.x = -point.v.x

            # y
            point.v.y += (point.f.y/self.mass) * dt
            point.y += point.v.y * dt

            # boundaries y
            if point.y > SCRSIZEY:
                point.y = SCRSIZEY
                point.v.y = -0.1*point.v.y
            elif point.y < 0:
                point.y = 0
                point.v.y = -0.1*point.v.y
            for slope in arr:
                if slope.point_in((point.x, point.y)):
                    point.y -= point.v.y*dt
                    point.v.y = -point.v.y

    def update(self, arr):
        self.gravity()
        self.spring_linear_force()
        self.pressure_force()
        self.newtons_equation(arr)
        # if self.pressure < self.max_pressure:
        #     self.pressure += 1.0

    def draw(self, screen, colour):
        for point in self.points:
            pygame.draw.circle(screen, colour, (point.x, point.y),  1)

    def draw_springs(self, screen, colour):
        for spring in self.springs:
            i, j = spring.i, spring.j
            x1 = self.points[i].x
            y1 = self.points[i].y
            x2 = self.points[j].x
            y2 = self.points[j].y
            pygame.draw.aaline(screen, colour, (x1, y1), (x2, y2))

    def draw_point_forces(self, screen, colour):
        for point in self.points:
            x, y = point.x, point.y
            px = point.f.x
            py = point.f.y
            # print(f'x = {px}, y = {py}')
            pygame.draw.aaline(screen, colour, (x, y), (x+px, y+py))
