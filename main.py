import pygame
import sys
import math
import random
import time as tm
import softbody.classes as sf
import softbody.othersoft as osf

import objects as phys
import functions as fn

mainClock = pygame.time.Clock()

screen_size = [1600,900]

black = (0, 0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0, 255)
blue = (0,0,255,255)
green = (0, 255 , 0)
red = (255 , 0, 0)
grey = (10,10,10,255)

pygame.init()


pygame.display.set_caption('pygame softbody')
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
screen.fill(white)

mouse_down = False

# arr = [phys.Point(100,100), phys.Point(110, 120), phys.Point(140, 130), phys.Point(150, 120)]
# rope = phys.Rope(arr)

object_arr = []
# object_arr.append(phys.Object(400, 400, phys.Circle(400, 400, 15), 10))
# ball = sf.ball(10, 100, 100, 50, 1)
ball = osf.Ball(400, 100, 15)
m = 1
s_down = False
while True:
    screen.fill(white)

    start = tm.time()

    ball.updatePhysics()
    # ball.draw_springs(screen, blue)
    ball.draw(screen, black)

    # ball.update()
    # ball.draw(screen, black)

    # ball.draw_point_forces(screen, red)
    # for spring in ball.springs:
    #     print(spring.length)
    # for point in rope.points:
    #     point.draw(screen)
    # for i in range(len(rope.points)-1):
    #     pygame.draw.line(screen, black, (rope.points[i].x, rope.points[i].y), (rope.points[i+1].x, rope.points[i+1].y))
    #
    # rope.update()
    # rope.IntegrateEuler()
    #
    # for object in ball_arr:
        # object.draw(screen)
        # object.update()
        # for i in range(19):
        #     pygame.draw.line(screen, black, (object.points[i].x, object.points[i].y), (object.points[i+1].x, object.points[i+1].y))
        # pygame.draw.line(screen, black, (object.points[0].x, object.points[0].y), (object.points[-1].x, object.points[-1].y))
        # object.draw_point_forces(screen)
        # # for i in range(10):
        #     print(object.springs[i].length)
        # print('n')
        # object.draw_forces(screen)
    end = tm.time()
    # print(f"{round((end - start), 5)}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            # ball_arr.append(phys.Ball(x, y, 20, 40))
            mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

        if event.type == pygame.KEYDOWN:
            if event.unicode == 's':
                s_down = True
            x,y = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP:
            if event.unicode == 's':
                s_down = False
    #
    if s_down:
        x,y = pygame.mouse.get_pos()
        for point in ball.myPoints:
            mx = (x-point.x)
            my = (y-point.y)
            print(mx)
            print(my)
            point.vx+=mx/100
            point.vy+=my/20

    pygame.display.update()
    mainClock.tick(120)
