import pygame
import math

class UniversalContainer:

    x = int
    y = int

    width = int
    height = int

    headerY = int

    components = []

    mouseOffsetX = 0
    mouseOffsetY = 0

    #STATES
    selected = False
    minimized = False

    resizeX = False
    resizeY = False

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.headerY = 10

    def min_size(self):
        maxX = 0
        maxY = 0
        for component in self.components:
            if (component.x+component.width) > maxX:
                maxX = component.x+component.width
            if (component.y+component.height) > maxY:
                maxY = component.y+component.height

        if self.width < maxX*1.2:
            self.width = maxX*1.2
        if self.height < maxY*1.2:
            self.height = maxY*1.2

    def resize(self, event):
        x, y = pygame.mouse.get_pos()
        if self.resizeX and event.type == pygame.MOUSEBUTTONUP:
            self.resizeX = False
        if self.resizeY and event.type == pygame.MOUSEBUTTONUP:
            self.resizeY = False

        if self.resizeX:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
            self.width = x-self.x
        if self.resizeY:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_SIZENS)
            self.height = y-self.y

        if (self.x+self.width-3 < x < self.x+self.width+3) and (self.y < y < self.y+self.height):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.resizeX = True
        elif (self.x < x < self.x+self.width) and (self.y+self.height-3 < y < self.y+self.height+3):
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_SIZENS)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.resizeY = True
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def render(self, screen, colour, font):
        pygame.draw.rect(screen, colour, (self.x, self.y, self.width, -self.headerY), width=3)
        if self.minimized==False:
            pygame.draw.rect(screen, colour, (self.x, self.y, self.width, self.height), width=1)
            for component in self.components:
                component.render(screen, colour, font, self.x, self.y)
                pass

    def coords_in(self,coords):
        x, y = coords
        if (self.x < x < self.x+self.width) and (self.y < y < self.y+self.height):
            return True
        else:
            return False

    def coords_in_header(self, coords):
        x, y = coords
        if (self.x < x < self.x+self.width) and (self.y-self.headerY < y < self.y):
            return True
        else:
            return False

    def check_input(self, event):
        if self.minimized == False:
            for component in self.components:
                component.check_input(event, self.x, self.y)
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_m) and self.coords_in_header(pygame.mouse.get_pos()):
                if self.minimized == False:
                    self.minimized = True
                else:
                    self.minimized = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.coords_in_header(pygame.mouse.get_pos()):
                x, y = pygame.mouse.get_pos()
                self.mouseOffsetX = x - self.x
                self.mouseOffsetY = y - self.y
                self.selected = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.selected:
                self.mouseOffsetX = 0
                self.mouseOffsetY = 0
                self.selected = False
        if self.selected:
            x, y = pygame.mouse.get_pos()
            self.x = x - self.mouseOffsetX
            self.y = y - self.mouseOffsetY
            if event.type == pygame.MOUSEBUTTONUP:
                self.selected = False
        self.resize(event)
        self.min_size()
        pass

class LineEdit:

    x = int
    y = int

    width = 0
    height = 0

    text = ''

    selected = False
    editable = True

    def __init__(self, x, y, width, height, text = ''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def coords_in(self,coords, offsetX=0, offsetY=0):
        x, y = coords
        if (self.x+offsetX < x < self.x+offsetX+self.width) and (self.y+offsetY < y < self.y+offsetY+self.height):
            return True
        else:
            return False

    def render(self, screen, colour, font, offsetX=0, offsetY=0):
        text = font.render(self.text, False, colour)
        x, y = text.get_size()
        if text != '':
            self.height = y*1.5
        if text.get_width() > self.width:
            self.width = x*1.5
        if self.selected==False:
            pygame.draw.rect(screen, colour, (self.x+offsetX, self.y+offsetY, self.width, self.height), width=1)
        elif self.selected:
            pygame.draw.rect(screen, colour, (self.x+offsetX, self.y+offsetY, self.width, self.height), width=4)
        screen.blit(text, (self.x+(self.width-x)/2+offsetX, self.y+offsetY+(self.height-y)/2))

    def check_input(self, event, offsetX=0, offsetY=0):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.coords_in(pygame.mouse.get_pos(), offsetX, offsetY):
                x, y = pygame.mouse.get_pos()
                self.selected = True
            else:
                self.selected = False
        if (event.type == pygame.KEYDOWN) and self.selected:
            if pygame.key.name(event.key) == 'backspace':
                self.text = self.text[:-1]
            elif pygame.key.name(event.key) == 'space':
                self.text += ' '
            elif pygame.key.name(event.key) == 'return':
                self.selected = False
            else:
                self.text += str(pygame.key.name(event.key))
                pass

class Texture:

    x = int
    y = int

    width = 0
    height = 0

    image = ''

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def coords_in(self,coords, offsetX=0, offsetY=0):
        x, y = coords
        if (self.x+offsetX < x < self.x+offsetX+self.width) and (self.y+offsetY < y < self.y+offsetY+self.height):
            return True
        else:
            return False

    def resize(self, width, height):
        pygame.transform.scale(self.image, (width, height))

    def render(self, screen, colour, font='', offsetX=0, offsetY=0):
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        screen.blit(self.image, (self.x+offsetX, self.y+offsetY))

    def check_input(self, event, offsetX=0, offsetY=0):
        pass

class Slider:
    x = int
    y = int

    width = 0
    height = 0

    min_value = 0
    max_value = 100

    value = 50

    selected = False

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def coords_in(self, coords, offsetX=0, offsetY=0):
        x_value = self.value*self.width/self.max_value
        x, y = coords
        if (self.x+offsetX+x_value-3 < x < self.x+offsetX+x_value+3) and (self.y+offsetY-3 < y < self.y+offsetY+self.height+3):
            return True
        else:
            return False

    def value_check(self):
        if self.value > self.max_value:
            self.value = self.max_value
        if self.value < self.min_value:
            self.value = self.min_value

    def render(self, screen, colour, font,  offsetX=0, offsetY=0):
        pygame.draw.rect(screen, colour, (self.x+offsetX, self.y+offsetY, self.width, self.height), width=1)
        x = self.value*self.width/self.max_value
        pygame.draw.rect(screen, colour, (self.x+x+offsetX-3, self.y+offsetY-3, 6, self.height+6))

    def check_input(self, event, offsetX=0, offsetY=0):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.coords_in(pygame.mouse.get_pos(), offsetX, offsetY):
                self.selected = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.selected:
                self.selected = False
        if self.selected:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_SIZENS)
            x, y = pygame.mouse.get_pos()
            value = (x-offsetX-self.x)*self.max_value/self.width
            self.value = value
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.value_check()

class Label:
    x = int
    y = int

    width = 0
    height = 0

    text = ''

    def __init__(self, x, y, text=''):
        self.x = x
        self.y = y
        # self.height = height
        # self.width = width
        self.text = text

    def render(self, screen, colour, font, offsetX=0, offsetY=0):
        text = font.render(self.text, False, colour)
        self.width = text.get_width()
        screen.blit(text, (self.x+offsetX, self.y+offsetY))

    def check_input(self, event, offsetX=0, offsetY=0):
        pass

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

    def __init__(self, x, y, width, height, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def render(self, screen, colour, font, offsetX=0, offsetY=0):
        text = font.render(self.text, False, colour)
        x, y = text.get_size()
        if self.text!='':
            self.width=x*1.5
        if self.pressed==False:
            pygame.draw.rect(screen, colour, (self.x+offsetX, self.y+offsetY, self.width, self.height), width=1)
        elif self.pressed:
            pygame.draw.rect(screen, colour, (self.x+offsetX, self.y+offsetY, self.width, self.height), width=4)
        screen.blit(text, (self.x+(self.width-x)/2+offsetX, self.y+offsetY+(self.height-y)/2))

    def coords_in(self,coords, offsetX=0, offsetY=0):
        x, y = coords
        if (self.x+offsetX < x < self.x+offsetX+self.width) and (self.y+offsetY < y < self.y+offsetY+self.height):
            return True
        else:
            return False

    def check_input(self, event, offsetX=0, offsetY=0):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.coords_in(pygame.mouse.get_pos(), offsetX, offsetY):
                self.pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
        if self.coords_in(pygame.mouse.get_pos(), offsetX, offsetY)==False:
            self.pressed = False

class Switch:

    x = int
    y = int
    height = int
    width = int

    #TEXT PROPERTIES
    text = ''
    font_size = 12

    #STATES
    pressed = False

    def __init__(self, x, y, width, height, text = ''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def render(self, screen, colour, font, offsetX=0, offsetY=0):
        text = font.render(self.text, False, colour)
        x, y = text.get_size()
        if self.text!='':
            self.width=x*1.5
        if self.pressed==False:
            pygame.draw.rect(screen, colour, (self.x+offsetX, self.y+offsetY, self.width, self.height), width=1)
        elif self.pressed:
            pygame.draw.rect(screen, colour, (self.x+offsetX, self.y+offsetY, self.width, self.height), width=4)
        screen.blit(text, (self.x+(self.width-x)/2+offsetX, self.y+offsetY+(self.height-y)/2))

    def coords_in(self,coords, offsetX=0, offsetY=0):
        x, y = coords
        if (self.x+offsetX < x < self.x+offsetX+self.width) and (self.y+offsetY < y < self.y+offsetY+self.height):
            return True
        else:
            return False

    def check_input(self, event, offsetX=0, offsetY=0):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.coords_in(pygame.mouse.get_pos(), offsetX, offsetY):
                if self.pressed:
                    self.pressed = False
                else:
                    self.pressed = True
