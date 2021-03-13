import pygame
import sys
import math
import random
import time as tm
import softbody.classes as sf
import ui.classes as ui

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

myfont = pygame.font.SysFont('timesnewroman',  12)

pygame.display.set_caption('pygame physV2')
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
screen.fill(white)

#STATES
mouse_down = False
object_selected = 0
object_picked = False

timer_label = ui.Label(10, 10, "timer label")

#ARRAYS
object_arr = [phys.Object(800, 100, phys.Circle(800, 100, 20), 1, False), phys.Object(0, 890, phys.Rect(0, 890, 1600, 10), 1, True)]
ui_arr = [timer_label]


s_down = False
while True:
    screen.fill(white)

    start = tm.time()

    #Drawing object array
    for object in object_arr:
        object.update(object_arr)
        object.draw_forces(screen)
        object.draw(screen)

    end = tm.time()
    timer_label.text = f"{round((end - start), 5)}"

    for element in ui_arr:
        element.render(screen, black, myfont)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        for element in ui_arr:
            element.check_input(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            for object in object_arr:
                if object.coords_in(pygame.mouse.get_pos()):
                    object_picked = True
                    object_selected = object

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
        mx = (x-object_selected.x)
        my = (y-object_selected.y)
        object_selected.v.x += mx/10
        object_selected.v.y += my/10
    # if s_down:
        # x,y = pygame.mouse.get_pos()
        # for point in ball.points:
        #     mx = (x-point.x)
        #     my = (y-point.y)
        #     point.v.x+=mx/100
        #     point.v.y+=my/20

    pygame.display.update()
    mainClock.tick(360)
