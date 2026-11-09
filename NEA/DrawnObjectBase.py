'''

this is the main class for all drawn objects in this game

'''
import pygame

from Base import Base

class DrawnObjectBase(Base):
    def __init__(self, client ,pos, type, colour, rect):
        super().__init__(pos, type, client)

        self.rect = rect
        self.colour = tuple(min(255, value + 30) for value in colour)

    def update(self, renderList, dt, typing, mousePos):
        renderList.append([self.type, self.colour, self.rect])