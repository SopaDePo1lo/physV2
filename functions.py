import math
import pygame
import objects as phys
import softbody.classes as sf
import ui.classes as ui

black = (0, 0, 0, 255)
white = (255, 255, 255)

def min_max_ball(ball):
    max_x = 0
    max_y = 0
    min_x = 1000
    min_y = 1000
    for point in ball.points:
        if point.x > max_x:
            max_x = point.x
        if point.x < min_x:
            min_x = point.x
        if point.y > max_y:
            max_y = point.y
        if point.y < min_y:
            min_y = point.y
    x = (max_x - min_x)*1.2
    y = (max_y - min_y)*1.2
    offsetX = (x - (max_x - min_x))/2
    offsetY = (y - (max_y - min_y))/2
    screen = pygame.surface.Surface((x, y))
    screen.fill(white)
    ball.draw_springs(screen, black, min_x-offsetX, min_y-offsetY)
    return screen

def create_triangle(arr, fy1, fy2):
    arr.append(sf.slope(fy2, fy1))
    return arr

def pressure_display(arr, label):
    sum = 0
    selected = 0
    for ball in arr:
        if ball.selected:
            selected = ball
            sum += 1
    if sum == 0:
        label.text = 'no ball selected'
    else:
        label.text = f'ball pressure = {str(selected.pressure)}'

def slider_modifier(slider, label, name):
    label.text = f'{name} = {slider.value}'

def pressure_modifier(add, remove, arr, slider, dif = 0.1):
    selected = 0
    for ball in arr:
        if ball.selected:
            selected = ball
    if selected != 0:
        if add.pressed:
            selected.pressure += dif
        if remove.pressed:
            selected.pressure -= dif
        slider.value = selected.pressure

def pressure_slider_modifier(slider, arr):
    selected = 0
    for ball in arr:
        if ball.selected:
            selected = ball
    if selected != 0:
        selected.pressure = slider.value
