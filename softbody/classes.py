import math
import pygame


SCRSIZEX, SCRSIZEY = 1600,900

ks = 4
kd = 0.5
dt = 0.05

class point:
    x = 0
    y = 0

    vx = 0.0
    vy = 0.0

    fx = 0.0
    fy = 0.0

    def __init__(self, xy, v, f):
        self.x, self.y = xy
        self.vx, self.vy = v
        self.fx, self.fy = f

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

class ball:

    pt_amount = 0
    points = []
    springs = []
    radius = 0.0
    mass = 1.0
    volume = 0.0
    pressure = 7.5 #default should be 10.0, if you want more buoyancy then set it to a lower value, if you want it more deflated then icrease the value !!MUST BE MORE THAN MAX_PRESSURE
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
                    self.addSpringCust(j,i)
        # # for i in range(points-1):
        # #     self.AddSpring(i, i, i+1)
        # self.AddSpring(-1, -1, 0)

    def addSpringCust(self,i,j):
        pA,pB = self.points[i],self.points[j]
        length = math.sqrt((pA.x - pB.x) *
                         (pA.x - pB.x) +
                         (pA.y - pB.y) *
                         (pA.y - pB.y))
        s = spring((i, j), length, (0,0))
        self.springs.append(s)


    def gravity(self):
        for point in self.points:
            point.fx = 0
            point.fy = self.mass * 9.8 *(self.pressure-self.max_pressure)

    def spring_linear_force(self):
        for spring in self.springs:
            i, j = spring.i, spring.j
            x1 = self.points[i].x
            y1 = self.points[i].y
            x2 = self.points[j].x
            y2 = self.points[j].y

            r12d = math.sqrt((x1 -x2)**2 + (y1-y2)**2)

            if r12d != 0:
                vx12 = self.points[i].vx - self.points[j].vx
                vy12 = self.points[i].vy - self.points[j].vy

            f = (r12d - spring.length)*ks + (vx12*(x1-x2) + vy12*(y1-y2))*kd/r12d

            fx = ((x1-x2)/r12d)*f
            fy = ((y1-y2)/r12d)*f

            self.points[i].fx -= fx
            self.points[i].fy -= fy
            self.points[j].fx += fx
            self.points[j].fy += fy

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

            self.points[i].fx += spring.nx*pressurev
            self.points[i].fy += spring.ny*pressurev
            self.points[j].fx += spring.nx*pressurev
            self.points[j].fy += spring.ny*pressurev

    def newtons_equation(self):
        for point in self.points:
            point.vx += (point.fx/self.mass)*dt
            point.x += point.vx*dt
            if point.x > SCRSIZEX:
                point.x = SCRSIZEX
                point.vx = -point.vx

            # y
            point.vy += (point.fy/self.mass) * dt
            point.y += point.vy * dt

            # boundaries y
            if point.y > SCRSIZEY:
                point.y = SCRSIZEY
                point.vy = -0.1*point.vy

    def update(self):
        self.gravity()
        self.spring_linear_force()
        self.pressure_force()
        self.newtons_equation()
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
            px = point.vx
            py = point.vy
            # print(f'x = {px}, y = {py}')
            pygame.draw.aaline(screen, colour, (x, y), (x+px, y+py))

    def AddSpring(self, pi, i, j):
        indexes = (i, j)
        length = math.sqrt((self.points[i].x - self.points[j].x)**2 + (self.points[i].y - self.points[j].y)**2)
        spr = spring(indexes, length, (0.0, 0.0))
        self.springs[pi] = spr
