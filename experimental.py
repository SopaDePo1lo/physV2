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
screen2 = pygame.surface.Surface((screen_size[0], screen_size[1]))
screen.fill(white)

#STATES
mouse_down = False
object_selected = 0
object_picked = False
s_down = False

#OBJECT VARRIABLES
timer_label = ui.Label(10, 10, "timer label")
# floor = kin.Rect(0, 890, 1600, 10, 1)
button = ui.ButtonChanged(10, 50, 100, 20)
button.text = 'reset pendulum'
button_save = ui.ButtonChanged(10, 80, 100, 20)
button_save.text = 'save screen'
button_clear = ui.ButtonChanged(10, 100, 100, 20)
button_clear.text = 'clear pendulum path'
# floor.static = True
screen2.fill(white)
double_pendulum = pd.DoublePendulum((500, 200), 1.0, 1.5, 100, 100, math.radians(90),  math.radians(90))
double_pendulum2 = pd.DoublePendulum((500, 200), 1.0, 1.5, 100, 100, math.radians(90.01),  math.radians(90))


#ARRAYS
object_arr = [kin.Rect((300, 840), 50, 50, 1), kin.Rect((000, 890), 1600, 10, 1, True)]
ui_arr = [timer_label, ui.Label(10, 30, "experimental scene"), button, button_save, button_clear]

while True:
    screen.fill(white)
    screen.blit(screen2, (0,0))

    start = tm.time()

    double_pendulum.update()
    double_pendulum2.update()
    double_pendulum.draw_point(screen2, red)
    double_pendulum2.draw_point(screen2, blue)
    double_pendulum2.draw(screen, black)
    double_pendulum.draw(screen, black)
    # Drawing object array

    for object in object_arr:
    #     # object.draw_forces(screen)
        object.update(object_arr)
    #     object.draw_forces(screen, blue)
        object.draw(screen, black)

    end = tm.time()
    timer_label.text = f"{round((end - start), 5)}"

    for element in ui_arr:
        element.render(screen, black, myfont)

    if button.pressed:
        double_pendulum.a1 = math.radians(60)
        double_pendulum.a2 = math.radians(60)
        double_pendulum.a1_v = 0.0
        double_pendulum.a2_v = 0.0
        double_pendulum.a1_a = 0.0
        double_pendulum.a2_a = 0.0

    if button_save.pressed:
        pygame.image.save(screen2, 'screenshots/img.png')
        button_save.pressed = False

    if button_clear.pressed:
        screen2.fill(white)
        button_clear.pressed=False

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
                    print('int')
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
        x,y = pygame.mouse.get_pos()
        mx = (x-object_selected.position.x)
        my = (y-object_selected.position.y)
        object_selected.velocity.x += mx/50
        object_selected.velocity.y += my/50
    # if s_down:
    #     x,y = pygame.mouse.get_pos()
    #     point = object_arr[0]
    #     mx = (x-point.x)
    #     my = (y-point.y)
    #     point.v.x+=mx/20
    #     point.v.y+=my/20

    pygame.display.update()
    mainClock.tick(300)
