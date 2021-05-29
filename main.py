import pygame
import sys
import math
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

#OBJECTS
ball1 = sf.ball(10, 600, 100, 40, 1)
ball2 = sf.ball(5, 400, 100, 20, 1)
timer_label = ui.Label(10, 10, "timer label")
ui_container = ui.UniversalContainer(1300, 50, 200, 300)
pressure_label = ui.Label(10, 30, "pressure label")
add_pr =  ui.Button(10, 60, 30, 15)
remove_pr = ui.Button(10, 80, 30, 15)

#ARRAYS
# slope_arr = [sf.slope((1000, 900), (1600, 400)), sf.slope((1000, 700), (0, 200))]
slope_arr = [sf.slope((820, 900), (1600, 400)), sf.slope((1000, 700), (0, 200))]
rope_arr = [sf.Rope(20, 800, 300, 20)]
# slope_arr = [sf.slope((1000, 900), (0, 400))]
ui_container.components = [pressure_label, add_pr, remove_pr]
ui_arr = [ ui.Button(10, 30, 80, 20),ui_container]
ui_arr[1].text = 'create triangle'
ball_arr = [ball1, ball2]

s_down = False
mouse_down = False

while True:  #main loop
    screen.fill(white)

    for ball in ball_arr:
        if ball.selected:
            pressure_label.text = str(ball.pressure)

    start = tm.time()

    for slope in slope_arr:
        slope.draw(screen, black)

    for rope in rope_arr:
        rope.draw(screen, black)
        for ball in ball_arr:
            rope.update(slope_arr, ball)
        rope.draw_point_forces(screen, red)

    for ball in ball_arr:
        ball.update(slope_arr, rope_arr)
        ball.draw_point_forces(screen, red)
        if ball.selected:
            ball.draw_springs(screen, green)
        else:
            ball.draw_springs(screen, black)


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
            for ball in ball_arr:
                if ball.point_in(x, y):
                    if ball.selected:
                        ball.selected = False
                    else:
                        ball.selected = True
                    print('in')
                    mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
            if object_picked:
                mouse_down = False
                object_selected=0
                object_picked=False

        if event.type == pygame.KEYDOWN:
            if event.unicode == 's':
                s_down = True
            x,y = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP:
            if event.unicode == 's':
                s_down = False

    if add_pr.pressed:
        for ball in ball_arr:
            if ball.selected:
                ball.pressure += 0.1
    if remove_pr.pressed:
        for ball in ball_arr:
            if ball.selected:
                ball.pressure -= 0.1

    if object_picked:
        pass

    # if mouse_down:
    #     x,y = pygame.mouse.get_pos()
    #     for point in ball.points:
    #         mx = (x-point.x)
    #         my = (y-point.y)
    #         point.v.x+=mx/100
    #         point.v.y+=my/20

    pygame.display.update()
    mainClock.tick(360)
