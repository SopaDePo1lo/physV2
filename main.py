import pygame
import sys
import math
import random
import time as tm
import softbody.classes as sf

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
object_selected = 0
object_picked = False

# slope_arr = [sf.slope((1000, 900), (1600, 400)), sf.slope((1000, 700), (0, 200))]
slope_arr = [sf.slope((820, 900), (1600, 400)), sf.slope((1000, 700), (0, 200))]
rope_arr = [sf.Rope(10, 1400, 100, 10)]
# slope_arr = [sf.slope((1000, 900), (0, 400))]

# arr = [phys.Point(100,100), phys.Point(110, 120), phys.Point(140, 130), phys.Point(150, 120)]
# rope = phys.Rope(arr)
# object_arr = [phys.Object(800, 100, phys.Circle(800, 100, 20), 1, False), phys.Object(0, 890, phys.Rect(0, 890, 1600, 10), 1, True)]
# object_arr = [phys.Object(300, 400, phys.Rect(300, 400, 100, 20), 1, False), phys.Object(300, 100, phys.Circle(300, 100, 20), 1, False), phys.Object(400, 500, phys.Circle(400, 500, 20), 1, False), phys.Object(300, 150, phys.Circle(300, 150, 5), 1,  False), phys.Object(0, 890, phys.Rect(0, 890, 1600, 10), 1, True)]
# object_arr.append(phys.Object(400, 400, phys.Circle(400, 400, 15), 10))
ball = sf.ball(10, 800, 100, 40, 1)

s_down = False
while True:
    screen.fill(white)

    start = tm.time()
    # for object in object_arr:
    #     object.update(object, object_arr)
    #     object.draw_forces(screen)
    #     object.draw(screen)
    for slope in slope_arr:
        slope.draw(screen, black)

    for rope in rope_arr:
        rope.draw(screen, black)
        rope.update()
        rope.draw_point_forces(screen, red)

    ball.update(slope_arr)
    ball.draw_point_forces(screen, red)
    ball.draw_springs(screen, black)
    # ball.draw(screen, red)

    end = tm.time()
    print(f"{round((end - start), 5)}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            # for object in object_arr:
            #     if object.coords_in(pygame.mouse.get_pos()):
            #         object_picked = True
            #         object_selected = object
            mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
            if object_picked:
                object_selected=0
                object_picked=False

        if event.type == pygame.KEYDOWN:
            if event.unicode == 's':
                s_down = True
            x,y = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP:
            if event.unicode == 's':
                s_down = False

    if object_picked:
        x,y = pygame.mouse.get_pos()
        # for object in object_arr:
        #     if object==object_selected:
        #         object.external_forces(phys.Vector(x-object.x, y-object.y))
        #         object.x = x
        #         object.y = y
                # object.f.x = -(object.x-x)
                # object.f.y = -(object.y-y)
                # pygame.draw.aaline(screen, blue, (object.x, object.y), (object.x -(object.x-x), object.y-(object.y-y)))
    #
    if s_down:
        x,y = pygame.mouse.get_pos()
        for point in ball.points:
            mx = (x-point.x)
            my = (y-point.y)
            point.v.x+=mx/100
            point.v.y+=my/20

    pygame.display.update()
    mainClock.tick(360)
