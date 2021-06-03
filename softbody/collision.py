import math
import pygame
import softbody.classes as sf

def ball_to_ball_collision(ball, arr):
    for collider in arr:
        if collider != ball:
            for point in collider.points:
                if ball.point_in(point.x, point.y):
                    return True
    return False
