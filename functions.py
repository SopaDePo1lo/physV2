import math
import objects as phys
import softbody.classes as sf
import ui.classes as ui

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

def pressure_modifier(add, remove, arr, dif = 0.1):
    selected = 0
    for ball in arr:
        if ball.selected:
            selected = ball
    if add.pressed:
        selected.pressure += dif
    if remove.pressed:
        selected.pressure -= dif

def pressure_slider_modifier(slider, arr):
    selected = 0
    for ball in arr:
        if ball.selected:
            selected = ball
    if selected != 0:
        selected.pressure = slider.value
