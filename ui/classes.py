import pygame
import math

class UniContainer:

    x = int
    y = int

    width = int
    height = int

    components = []

    selected = False
    draw_tr = False

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, screen, colour, font):
        pygame.draw.rect(screen, colour, (self.x, self.y, self.width, self.height), width=2)
        for component in self.components:
            component.render(screen, colour, font, self.x, self.y)
            pass

    def coords_in(self,coords):
        x, y = coords
        if (self.x < x < self.x+self.width) and (self.y < y < self.y+self.height):
            return True
        else:
            return False

    def check_input(self, event):
        # if self.selected:
        #     x, y =pygame.mouse.get_pos()
        #     self.x = x
        #     self.y = y
        #     if event.type == pygame.MOUSEBUTTONUP:
        #         self.selected = False
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if self.coords_in(pygame.mouse.get_pos()):
        #         self.selected = True
        pass

class Label:
    x = int
    y = int
    # width = int
    # height = int
    draw_tr = False

    text = ''

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        # self.height = height
        # self.width = width
        self.text = text

    def render(self, screen, colour, font, offsetX=0, offsetY=0):
        text = font.render(self.text, False, colour)
        screen.blit(text, (self.x+offsetX, self.y+offsetY))

    def check_input(self, event):
        pass

class ButtonChanged:

    x = int
    y = int
    height = int
    width = int

    #TEXT PROPERTIES
    text = ''
    font_size = 12

    #STATES
    pressed = False
    draw_tr = False

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, screen, colour, font, offsetX=0, offsetY=0):
        if self.text!='':
            self.width=len(self.text*self.font_size)/2
        if self.pressed==False:
            pygame.draw.rect(screen, colour, (self.x+offsetX, self.y+offsetY, self.width, self.height), width=1)
        elif self.pressed:
            pygame.draw.rect(screen, colour, (self.x+offsetX, self.y+offsetY, self.width, self.height), width=4)
        text = font.render(self.text, False, colour)
        screen.blit(text, (self.x+self.font_size/2+offsetX, self.y+offsetY))

    def coords_in(self,coords):
        x, y = coords
        if (self.x < x < self.x+self.width) and (self.y < y < self.y+self.height):
            return True
        else:
            return False

    def check_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.coords_in(pygame.mouse.get_pos()):
                self.pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
        if self.coords_in(pygame.mouse.get_pos())==False:
            self.pressed = False

class Button:

    x = int
    y = int
    height = int
    width = int

    #TEXT PROPERTIES
    text = ''
    font_size = 12

    #STATES
    pressed = False
    num = 3
    frst = tuple
    second = tuple
    draw_tr = False

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, screen, colour, font, offsetX=0, offsetY=0):
        if self.text!='':
            self.width=len(self.text*self.font_size)/2
        if self.pressed==False:
            pygame.draw.rect(screen, colour, (self.x+offsetX, self.y+offsetY, self.width+offsetX, self.height+offsetY), width=1)
        elif self.pressed:
            pygame.draw.rect(screen, colour, (self.x+offsetX, self.y+offsetY, self.width+offsetX, self.height+offsetY), width=4)
        text = font.render(self.text, False, colour)
        screen.blit(text, (self.x+offsetX, self.y+offsetY))

    def coords_in(self,coords):
        x, y = coords
        if (self.x < x < self.x+self.width) and (self.y < y < self.y+self.height):
            return True
        else:
            return False

    def check_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.coords_in(pygame.mouse.get_pos()):
                self.pressed = True
        if self.pressed == True:
            if self.num == 0:
                self.pressed = False
                self.num = 3
                self.draw_tr = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.num == 2:
                    self.frst = pygame.mouse.get_pos()
                elif self.num == 1:
                    self.second = pygame.mouse.get_pos()
                self.num-=1
        # if event.type == pygame.MOUSEBUTTONUP:
        #     self.pressed = False
        # if self.coords_in(pygame.mouse.get_pos())==False:
        #     self.pressed = False
