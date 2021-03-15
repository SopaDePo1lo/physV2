import math
import kinematic.classes as phys
import ui.classes as ui

def collision(object, array):
    object_type = type(object)
    for body in array:
        if object!=body:
            if type(body) == phys.Circle:
                if object_type == phys.Circle:
                    if circle_to_circle_collision(object, body):
                        force_exchange(object, body)
                        return True
                elif object_type == phys.Rect:
                    if circle_to_rect_collision(body, object):
                        force_exchange(body, object)
                        return True
            elif type(body) == phys.Rect:
                if object_type == phys.Circle:
                    if circle_to_rect_collision(object, body):
                        force_exchange(object, body)
                        return True
                elif object_type == phys.Rect:
                    if rect_to_rect_collision(object, body):
                        force_exchange(object, body)
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
        # object.v.x -= object.v.x*body.friction*object.width/10
        return True
    else:
        return False

def circle_to_rect_collision(object, body):
    dx = abs(object.x - body.x -(body.width/2))
    dy = abs(object.y - body.y - (body.height/2))
    # if body.static==False and object.static==False:
    #     vx = object.v.x+body.v.x
    # else:
    #     vx = object.v.x
    if (dx > ((body.width/2) + object.radius)):
        return False
    if (dy >= ((body.height/2) + object.radius)):
        return False
    if (dx < (body.width/2)):
        # if body.static==False and object.static==False:
        #     print('change vx')
        #     object.v.x -= vx/2
        #     body.v.x +=  vx/2
        return True
    if (dy < (body.height/2)):
        # if body.static==False and object.static==False:
        #     print('change vx')
        #     object.v.x -= vx/2
        #     body.v.x +=  vx/2
        return True
    kx = dx - (body.width/2)
    ky = dy - (body.height/2)
    if (kx**2 + ky**2) < (object.radius**2):
        # if body.static==False and object.static==False:
        #     print('change vx')
        #     object.v.x -= vx/2
        #     body.v.x +=  vx/2
        return True

def rect_to_circle_collision(body, object):
    dx = abs(object.x - body.x -(body.width/2))
    dy = abs(object.y - body.y - (body.height/2))
    vx = object.v.x
    if (dx > ((body.width/2) + object.radius)):
        return False
    if (dy >= ((body.height/2) + object.radius)):
        return False
    if (dx < (body.width/2)):
        object.v.x -= vx*body.friction/2
        body.v.x +=  vx/2
        return True
    if (dy < (body.height/2)):
        object.v.x -= vx*body.friction/2
        body.v.x +=  vx/2
        return True
    kx = dx - (body.width/2)
    ky = dy - (body.height/2)
    if (kx**2 + ky**2) < (object.radius**2):
        object.v.x -= vx*body.friction/2
        body.v.x +=  vx/2
        return True

def force_exchange(object, body):
    if body.static == False and object.static == False:
        vx = body.v.x+object.v.x
        vy = body.v.y+object.v.y
        body.v.x += vx/2
        object.v.x -= vx/2
        body.v.y += vy/2
        object.v.y -= vy/2
        print(1)
    elif body.static == False and object.static == True:
        vx = body.v.x
        vy = body.v.y
        body.v.x -= vx/2
        body.v.y -= vy/2
        print(2)
    elif body.static == True and object.static == False:
        print(object.v.y)
        object.v.y = -0.2*object.v.y
        print(object)
        print(object.v.y)
        print(3)
    else:
        pass


def circle_to_circle_collision(object, body):
    vx = object.v.x+body.v.x
    vy = object.v.y+body.v.y
    mx = object.x-body.x
    my = object.y-body.y
    m = math.sqrt(mx**2 + my**2)
    if m < object.radius+body.radius:
        return True
    else:
        return False
