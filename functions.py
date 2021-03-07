import math
import objects as phys

def collision(object, array):
    object_type = type(object)
    for body in array:
        if object!=body:
            if type(body) == phys.Circle:
                pass
            elif type(body) == phys.Rect:
                if object_type == phys.Circle:
                    if circle_to_rect_collision(object, body):
                        return True
                elif object_type == phys.Rect:
                    if rect_to_rect_collision(object, body):
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
    return ((kx**2 + ky**2) < (object.radius**2))
