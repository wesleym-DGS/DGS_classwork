'''
this is going to be the main class for the player object. It is going to need to use the Base class as its parent class
'''
import pygame

#using the Base class to avoid repeated code
from Base import Base

class Player(Base):
    def __init__(self):
        # passing the players type as a ellipsis
        super().__init__((0,0), 'E')

        #then creating this objects rect so it can be drawn
        self.rect = pygame.Rect(self.pos.x - 7.5, self.pos.y - 7.5, 15, 15)