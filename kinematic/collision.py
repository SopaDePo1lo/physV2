import math
import kinematic.classes as phys
import ui.classes as ui

def collision(collider, array):
    collider_type = type(collider)
    for body in array:
        if collider!=body:
            # if type(body) == phys.Circle:
            #     if collider_type == phys.Circle:
            #         if circle_to_circle_collision(collider, body):
            #             return True
            #     elif collider_type == phys.Rect:
            #         if circle_to_rect_collision(body, collider):
            #             return True
            if type(body) == phys.Rect:
                # if collider_type == phys.Circle:
                #     if circle_to_rect_collision(collider, body):
                #         return True
                if collider_type == phys.Rect:
                    if rect_to_rect_collision(collider, body):
                        force_exchange(collider, body)
                        return True
    return False

def rect_to_rect_collision(object, body):
    if body.coords_in((object.position.x, object.position.y)):
        return True
    elif body.coords_in((object.position.x+object.width, object.position.y)):
        return True
    elif body.coords_in((object.position.x, object.position.y+object.height)):
        return True
    elif body.coords_in((object.position.x+object.width, object.position.y+object.height)):
        return True
    else:
        return False

def circle_to_rect_collision(object, body):
    dx = abs(object.x - body.x -(body.width/2))
    dy = abs(object.y - body.y - (body.height/2))
    if (dx > ((body.width/2) + object.radius)):
        return False
    if (dy >= ((body.height/2) + object.radius)):
        return False
    if (dx < (body.width/2)):
        return True
    if (dy < (body.height/2)):
        return True
    kx = dx - (body.width/2)
    ky = dy - (body.height/2)
    if (kx**2 + ky**2) < (object.radius**2):
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

def force_exchange(collider, body):
    if body.static == False and collider.static == False:
        collider.velocity.x = -collider.velocity.x/2
        collider.velocity.y = -collider.velocity.y/2

        body.velocity.x = -body.velocity.x/2
        body.velocity.y = -body.velocity.y/2
    elif body.static == False and collider.static == True:
        vx = body.velocity.x
        vy = body.velocity.y
        body.velocity.x = -vx/2
        body.velocity.y = -vy/2
    elif body.static == True and collider.static == False:
        vx = collider.velocity.x
        vy = collider.velocity.y
        collider.velocity.x = -vx/2
        collider.velocity.y = -vy/2
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
