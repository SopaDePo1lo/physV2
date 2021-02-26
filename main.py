import pygame
import sys
import math
import random
import time as tm

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

object_arr = []
object_arr.append(phys.Object(400, 400, phys.Circle(400, 400, 15), 10))

m = 10

while True:
    screen.fill(white)

    start = tm.time()

    for object in object_arr:
        object.draw(screen)
        object.draw_forces(screen)

    end = tm.time()
    # print(f"{round((end - start), 5)}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            mouse_down = False

        if event.type == pygame.KEYDOWN:
            x,y = pygame.mouse.get_pos()


    pygame.display.update()
    mainClock.tick(60)
