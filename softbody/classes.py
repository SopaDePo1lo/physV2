import math
import pygame
import softbody.collision as cl

#https://panoramx.ift.uni.wroc.pl/~maq/soft2d/howtosoftbody.pdf

SCRSIZEX, SCRSIZEY = 1600,900

ks = 4
kd = 0.9
dt = 0.05

class point:
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

class Rope:

    points = []
    springs = []
    pt_amount = 0
    mass = 0.3

    def __init__(self, pt_amount, x, y, lenght):
        self.pt_amount = pt_amount
        for sect in range(pt_amount):
            self.points.append(point((x+sect*lenght, y), (0,0), (0,0)))
        self.points[0].static = True
        self.points[-1].static = True

        for i in range(pt_amount-1):
            length = math.sqrt((self.points[i].x - self.points[i+1].x) **2 + (self.points[i].y - self.points[i+1].y)**2)
            self.springs.append(spring((i, i+1),lenght, (0,0)))

    def draw(self, screen, colour):
        for point in self.points:
            pygame.draw.circle(screen, colour, (point.x, point.y), 1)
        for spring in self.springs:
            i, j = spring.i, spring.j
            pygame.draw.aaline(screen, colour, (self.points[i].x, self.points[i].y), (self.points[j].x, self.points[j].y))

    def update(self, arr, ball):
        self.gravity()
        self.spring_linear_force()
        self.IntegrateEuler(arr, ball)

    def draw_point_forces(self, screen, colour):
        for point in self.points:
            if point.static==False:
                pygame.draw.aaline(screen, colour, (point.x, point.y), (point.x+point.f.x, point.y+point.f.y))

    def gravity(self):
        for point in self.points:
            if point.static==False:
                point.f.x = 0
                point.f.y = self.mass * 9.8

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

    def point_colliding(self, point, obj):
        x, y = point
        for spring in self.springs:
            i, j = spring.i, spring.j
            x1 = self.points[i].x
            y1 = self.points[i].y
            x2 = self.points[j].x
            y2 = self.points[j].y

            m = -(y2-y1)/(x2-x1)

            if x1<=x<=x2 or x1>=x>=x2:
                xcol = x-x1
                ycol = y1-(xcol*m)
                # print(f'{x}, {int(ycol)}')
                # print(y)
                if int(y)==int(ycol):
                    self.points[i].v.x += obj.v.x/2
                    self.points[i].v.y += obj.v.y/2
                    self.points[j].v.x += obj.v.x/2
                    self.points[j].v.y += obj.v.y/2
                    return True

        return False


    def IntegrateEuler(self, arr, ball):
        for point in self.points:
            if point.static==False:
                point.v.x += (point.f.x/self.mass)*dt
                point.x += point.v.x*dt
                if point.x > SCRSIZEX:
                    point.x = SCRSIZEX
                    point.v.x = -point.v.x
                elif point.x < 0:
                    point.x=0
                    point.v.x = -point.v.x
                # if ball.point_in(point.x, point.y):
                #     point.v.x = -point.v.x
                #     point.x -= point.v.x*dt
                #     print('in')
                #     for pt in ball.points:
                #         pt.v.x += point.v.x/ball.pt_amount
                #         pt.v.y += point.v.y/ball.pt_amount
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
                # if ball.point_in(point.x, point.y):
                #     point.v.y = -point.v.y
                #     point.y -= point.v.y*dt
                #     for pt in ball.points:
                #         pt.v.x += point.v.x/ball.pt_amount
                #         pt.v.y += point.v.y/ball.pt_amount
                for slope in arr:
                    if slope.point_in((point.x, point.y)):
                        point.y -= point.v.y*dt
                        point.v.y = -point.v.y


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

    selected = False

    def __init__(self, points, x, y, radius, mass):
        self.pressure = 5.5
        self.points = []
        self.springs = []
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
        length = math.sqrt((self.points[i].x - self.points[j].x) **2 + (self.points[i].y - self.points[j].y)**2)
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

    def IntegrateEuler(self, arr, rope_arr, ball_arr):
        for point in self.points:
            point.v.x += (point.f.x/self.mass)*dt
            point.x += point.v.x*dt
            if point.x > SCRSIZEX:
                point.x = SCRSIZEX
                point.v.x = -point.v.x
            elif point.x < 0:
                point.x=0
                point.v.x = -point.v.x
            if cl.ball_to_ball_collision(self, ball_arr):
                point.x -= point.v.x*dt
                point.v.x = -point.v.x
            for slope in arr:
                if slope.point_in((point.x, point.y)):
                    point.x -= point.v.x*dt
                    point.v.x = -point.v.x
            for rope in rope_arr:
                if rope.point_colliding((point.x, point.y), point):
                    # print('col')
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
            if cl.ball_to_ball_collision(self, ball_arr):
                point.v.y = -point.v.y
                point.y -= point.v.y*dt
            for slope in arr:
                if slope.point_in((point.x, point.y)):
                    point.y -= point.v.y*dt
                    point.v.y = -point.v.y
            for rope in rope_arr:
                if rope.point_colliding((point.x, point.y), point):
                    # print('col')
                    point.y -= point.v.y*dt
                    point.v.y = -point.v.y

    def update(self, arr, rope_arr, ball_arr):
        self.gravity()
        self.spring_linear_force()
        self.pressure_force()
        self.IntegrateEuler(arr,rope_arr, ball_arr)
        # if self.pressure < self.max_pressure:
        #     self.pressure += 1.0

    def draw(self, screen, colour, offsetX=0, offsetY=0):
        for point in self.points:
            pygame.draw.circle(screen, colour, (point.x-offsetX, point.y-offsetY),  1)

    def draw_springs(self, screen, colour, offsetX=0, offsetY=0):
        for spring in self.springs:
            i, j = spring.i, spring.j
            x1 = self.points[i].x
            y1 = self.points[i].y
            x2 = self.points[j].x
            y2 = self.points[j].y
            pygame.draw.aaline(screen, colour, (x1+offsetX, y1+offsetY), (x2+offsetX, y2+offsetY))

    def point_in(self, x, y):
        n = len(self.points)
        inside = False

        p1x,p1y = self.points[0].x, self.points[0].y
        for i in range(n+1):
            p2x,p2y = self.points[i % n].x, self.points[i % n].y
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    def draw_point_forces(self, screen, colour):
        for point in self.points:
            x, y = point.x, point.y
            px = point.f.x
            py = point.f.y
            # print(f'x = {px}, y = {py}')
            pygame.draw.aaline(screen, colour, (x, y), (x+px, y+py))
