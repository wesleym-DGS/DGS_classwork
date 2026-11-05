'''

this is going to be the parent class for all buttons that are going to be rendered when the game is running

'''

import pygame

from Base import Base

class InGameButtonBase(Base):
    def __init__(self, text, client, pos, width, height, colour):

        #as this is an object that needs rendering it uses the base class
        super().__init__(pos, 'CB', client)

        #creating the font that the button uses when it gets rendered
        self.font = pygame.font.SysFont(None, 20)

        #assigning the color to the object
        self.colour = colour

        #assigning the text to the object
        self.text = text

        #making the rect that all the text and the colors get based around
        self.rect = pygame.Rect(self.pos.x, self.pos.y, width, height)

    def update(self, renderList, dt, typing):

        #happening the needed data to the render list so it can get rendered
        renderList.append([self.type, self.colour, self.rect, self.text, self.font])