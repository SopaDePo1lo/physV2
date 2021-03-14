import pygame
import sys
import math
import random
import time as tm
import softbody.classes as sf
import kinematic.classes as kin
import pendulum.classes as pd
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
s_down = False

#OBJECT VARRIABLES
timer_label = ui.Label(10, 10, "timer label")
floor = kin.Rect(0, 890, 1600, 10, 1)
floor.static = True
double_pendulum = pd.DoublePendulum((200, 200), 1, 1, 50, 50, 0.2, 0.2)

#ARRAYS
object_arr = [kin.Circle(800, 100, 20, 1),kin.Circle(1200, 100, 20, 10), floor, kin.Rect(300, 100, 50, 50, 1)]
# object_arr = [kin.Circle(800, 100, 20, 1), kin.Circle(1200, 100, 20, 10), floor]
ui_arr = [timer_label, ui.Label(10, 30, "experimental scene")]

while True:
    screen.fill(white)

    start = tm.time()

    double_pendulum.update()
    double_pendulum.draw(screen, black)
    #Drawing object array

    # for object in object_arr:
    #     # object.update(object_arr)
    #     # object.draw_forces(screen)
    #     object.update(object_arr)
    #     object.draw_forces(screen, blue)
    #     object.draw(screen, black)

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

    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         x,y = pygame.mouse.get_pos()
    #         for object in object_arr:
    #             if object.coords_in(pygame.mouse.get_pos()):
    #                 object_picked = True
    #                 object_selected = object
    #
    #     if event.type == pygame.MOUSEBUTTONUP:
    #         mouse_down = False
    #         if object_picked:
    #             object_selected=0
    #             object_picked=False
    #
    #     if event.type == pygame.KEYDOWN:
    #         if event.unicode == 's':
    #             s_down = True
    #         x,y = pygame.mouse.get_pos()
    #     if event.type == pygame.KEYUP:
    #         if event.unicode == 's':
    #             s_down = False
    #
    # if object_picked:
    #     x,y = pygame.mouse.get_pos()
    #     mx = (x-object_selected.x)
    #     my = (y-object_selected.y)
    #     object_selected.v.x += mx/50
    #     object_selected.v.y += my/50
    # if s_down:
    #     x,y = pygame.mouse.get_pos()
    #     point = object_arr[0]
    #     mx = (x-point.x)
    #     my = (y-point.y)
    #     point.v.x+=mx/20
    #     point.v.y+=my/20

    pygame.display.update()
    mainClock.tick(30)
