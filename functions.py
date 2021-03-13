import math
import objects as phys
import softbody.classes as sf
import ui.classes as ui

def create_triangle(arr, fy1, fy2):
    arr.append(sf.slope(fy2, fy1))
    return arr

def collision(object, array):
    object_type = type(object.type)
    for body in array:
        if object.type!=body.type:
            if type(body.type) == phys.Circle:
                if object_type == phys.Circle:
                    if circle_to_circle_collision(object.type, body.type):
                        return True
                elif object_type == phys.Rect:
                    if circle_to_rect_collision(body.type, object.type):
                        return True
            elif type(body.type) == phys.Rect:
                if object_type == phys.Circle:
                    if circle_to_rect_collision(object.type, body.type):
                        return True
                elif object_type == phys.Rect:
                    if rect_to_rect_collision(object.type, body.type):
                        return True
    return False

def rect_to_rect_collision(object, body):
    if body.coords_in((object.x, object.y)):
        return True
    elif body.coords_in((object.x+object.width, object.y)):
        return True
    elif body.coords_in((object.x, object.y+object.height)):
        return True
    elif body.coords_in((object.x+object.width, object.y+object.height)):
        return True
    else:
        return False

def circle_to_rect_collision(object, body):
    dx = abs(object.x - body.x -(body.width/2))
    dy = abs(object.y - body.y - (body.height/2))

    if (dx > ((body.width/2) + object.radius)):
        return False
    if (dy > ((body.height/2) + object.radius)):
        return False
    if (dx <= (body.width/2)):
        return True
    if (dy <= (body.height/2)):
        return True
    kx = dx - (body.width/2)
    ky = dy - (body.height/2)
    return ((kx**2 + ky**2) <= (object.radius**2))


def circle_to_circle_collision(object, body):
    mx = object.x-body.x
    my = object.y-body.y
    m = math.sqrt(mx**2 + my**2)
    if m <= object.radius+body.radius:
        return True
    else:
        return False
