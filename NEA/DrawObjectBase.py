
'''
this is the main class for all drawn objects in this game
'''

import pygame

from Base import Base


class DrawObjectBase(Base):
    def __init__(self, client, pos, mousePos, type, colour):
        super().__init__(pos, type, client)

        #converting the mouse position into a vector
        mousePos = pygame.Vector2(mousePos)

        #creating the rect based on the starting and current mouse positions
        self.rect = pygame.Rect(self.pos.x,self.pos.y,mousePos.x - self.pos.x,mousePos.y - self.pos.y)

        #making sure the rect has positive dimensions
        self.rect.normalize()

        self.colour = colour

    def update(self, renderList, dt, typing, mousePos):

        #converting the current mouse position into a vector
        mousePos = pygame.Vector2(mousePos)

        #updating the rect based on where the mouse currently is
        self.rect = pygame.Rect(self.pos.x,self.pos.y,mousePos.x - self.pos.x,mousePos.y - self.pos.y)

        #allowing the object to be drawn in any direction
        self.rect.normalize()

        #adding the object to the render list
        renderList.append([self.type, self.colour, self.rect])
